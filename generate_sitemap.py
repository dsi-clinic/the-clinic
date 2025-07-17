#!/usr/bin/env python3
"""Jekyll Site Map Generator

This script automatically generates a visual site map for Jekyll sites by:
1. Scanning all markdown files in the repository
2. Extracting internal links and references
3. Building a dependency graph
4. Outputting a Mermaid diagram

Usage:
    python generate_sitemap.py [--output sitemap.md] [--format mermaid|dot|json]
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

# Optional imports for different visualization backends
try:
    import graphviz

    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False

try:
    import matplotlib.patches as patches
    import matplotlib.pyplot as plt
    import networkx as nx

    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False


class JekyllSiteMapper:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.pages = {}
        self.links = {}
        self.external_links = {}

    def scan_markdown_files(self) -> List[Path]:
        """Find all markdown files in the Jekyll site"""
        md_files = []

        # Get all .md files, excluding _site and .venv directories
        for md_file in self.root_path.rglob("*.md"):
            if "_site" not in md_file.parts and ".venv" not in md_file.parts:
                md_files.append(md_file)

        return md_files

    def extract_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Extract YAML frontmatter from markdown content"""
        if not content.startswith("---"):
            return {}, content

        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}, content

        try:
            frontmatter = yaml.safe_load(parts[1])
            content = parts[2]
            return frontmatter or {}, content
        except yaml.YAMLError:
            return {}, content

    def extract_links(
        self, content: str, current_file: Path
    ) -> Tuple[List[str], List[str]]:
        """Extract internal and external links from markdown content"""
        import re
        internal_links = []
        external_links = []

                # Improved regex: match links even if split across lines or with extra whitespace
        markdown_links = re.findall(r"\[([^\]]+)\]\(([^)]+?)\)", content, re.DOTALL)
        for text, url in markdown_links:
            # Clean up the URL (remove quotes, whitespace)
            url = url.strip().strip("\"'")

            # Skip empty URLs
            if not url:
                continue

            # Skip anchors and external URLs
            if url.startswith("#"):
                continue
            elif (
                url.startswith("http://")
                or url.startswith("https://")
                or url.startswith("//")
            ):
                external_links.append(url)
            elif (
                url.startswith("mailto:")
                or url.startswith("tel:")
                or url.startswith("ftp:")
            ):
                external_links.append(url)
            else:
                # Remove fragment identifiers from internal links
                if "#" in url:
                    url = url.split("#")[0]
                    if not url:  # If it was just a fragment, skip it
                        continue

                # Convert to relative path from current file
                link_path = self.resolve_link_path(current_file, url)
                if link_path:
                    internal_links.append(link_path)
                else:
                    # For broken links, add the attempted path so we can detect them
                    # Try to construct a reasonable path for reporting
                    if url.startswith("../"):
                        # Remove ../ prefix and add to current file's parent directory
                        clean_url = url[3:]  # Remove "../"
                        attempted_path = str(current_file.parent.parent / clean_url)
                    elif url.startswith("./"):
                        # Remove ./ prefix
                        clean_url = url[2:]  # Remove "./"
                        attempted_path = str(current_file.parent / clean_url)
                    else:
                        # Regular relative path
                        attempted_path = str(current_file.parent / url)
                    
                    # Convert to relative path from root for consistency
                    try:
                        relative_attempted_path = str(Path(attempted_path).relative_to(self.root_path.resolve()))
                        internal_links.append(relative_attempted_path)
                    except ValueError:
                        # If we can't make it relative to root, just use the attempted path
                        internal_links.append(attempted_path)

        return internal_links, external_links

    def resolve_link_path(self, current_file: Path, link_url: str) -> str:
        """Resolve a link to a path relative to the site root"""
        original_url = link_url

        # Remove .html extension if present (Jekyll converts .md to .html)
        if link_url.endswith(".html"):
            link_url = link_url[:-5] + ".md"

        # Handle directory index files
        if link_url.endswith("/"):
            link_url += "index.md"

        # Determine if this is an absolute path (starts with /) or relative path
        if original_url.startswith("/"):
            # Absolute path - resolve relative to site root
            # Remove leading slash
            link_url = link_url[1:] if link_url.startswith("/") else link_url
            return self._try_resolve_from_root(link_url)
        else:
            # Relative path - resolve relative to current file's directory
            current_dir = current_file.parent

            # Handle explicit relative paths (./ or ../)
            if original_url.startswith("./"):
                # Remove ./ prefix but keep it relative to current dir
                link_url = (
                    link_url[2:] if link_url.startswith("./") else link_url
                )
                return self._try_resolve_from_dir(current_dir, link_url)
            elif original_url.startswith("../") or "../" in original_url:
                # Handle directory traversal
                return self._try_resolve_from_dir(current_dir, link_url)
            else:
                # Regular relative path - try current dir first, then root
                result = self._try_resolve_from_dir(current_dir, link_url)
                if result:
                    return result
                # If not found relative to current dir, try from root
                return self._try_resolve_from_root(link_url)

    def _try_resolve_from_dir(self, base_dir: Path, link_url: str) -> str:
        """Try to resolve a link from a specific directory"""
        try:
            # Resolve the path (handles .. and . properly)
            target_path = (base_dir / link_url).resolve()

            # Make sure the resolved path is still within the site root
            if (
                self.root_path.resolve() in target_path.parents
                or target_path == self.root_path.resolve()
            ):
                if target_path.exists():
                    return str(
                        target_path.relative_to(self.root_path.resolve())
                    )

                # Try with .md extension
                if not link_url.endswith(".md"):
                    target_path_md = target_path.with_suffix(".md")
                    if target_path_md.exists():
                        return str(
                            target_path_md.relative_to(
                                self.root_path.resolve()
                            )
                        )
        except (ValueError, OSError):
            # Path resolution failed (e.g., goes outside root)
            pass

        return None

    def _try_resolve_from_root(self, link_url: str) -> str:
        """Try to resolve a link from the site root"""
        try:
            target_path = self.root_path / link_url

            if target_path.exists():
                return str(target_path.relative_to(self.root_path))

            # Try with .md extension
            if not link_url.endswith(".md"):
                target_path_md = self.root_path / (link_url + ".md")
                if target_path_md.exists():
                    return str(target_path_md.relative_to(self.root_path))
        except (ValueError, OSError):
            pass

        return None

    def analyze_site(self):
        """Analyze the entire Jekyll site"""
        md_files = self.scan_markdown_files()

        for md_file in md_files:
            try:
                with open(md_file, encoding="utf-8") as f:
                    content = f.read()

                frontmatter, body = self.extract_frontmatter(content)
                internal_links, external_links = self.extract_links(
                    body, md_file
                )

                relative_path = str(md_file.relative_to(self.root_path))

                self.pages[relative_path] = {
                    "path": relative_path,
                    "title": frontmatter.get(
                        "title", self.get_title_from_content(body)
                    ),
                    "frontmatter": frontmatter,
                    "size": len(body),
                }

                self.links[relative_path] = internal_links
                self.external_links[relative_path] = external_links

            except Exception as e:
                print(f"Error processing {md_file}: {e}")

    def get_title_from_content(self, content: str) -> str:
        """Extract title from markdown content"""
        # Look for first # header
        lines = content.split("\n")
        for line in lines:
            if line.startswith("# "):
                return line[2:].strip()
        return "Untitled"

    def get_page_category(self, path: str) -> str:
        """Categorize pages based on their path"""
        if path == "README.md":
            return "main"
        elif "/" not in path:
            return "section"
        else:
            return "resource"

    def generate_mermaid(self) -> str:
        """Generate Mermaid diagram with improved layout"""
        # Use flowchart instead of graph for better control
        mermaid = ["flowchart TB"]

        # Create node definitions with shorter labels
        node_ids = {}
        counter = 0

        # Group pages by category for better organization
        main_pages = []
        section_pages = []
        resource_pages = []

        for path in self.pages:
            category = self.get_page_category(path)
            node_id = f"N{counter}"
            node_ids[path] = node_id

            # Create shorter, cleaner titles
            title = self.pages[path]["title"]
            clean_title = title.replace('"', "'").replace("\n", " ")

            # Shorten path for display
            display_path = path.replace(".md", "").replace("/", "/<br/>")

            if category == "main":
                main_pages.append((node_id, clean_title, display_path))
            elif category == "section":
                section_pages.append((node_id, clean_title, display_path))
            else:
                resource_pages.append((node_id, clean_title, display_path))

            counter += 1

        # Add nodes organized by category
        mermaid.append("    %% Main Pages")
        for node_id, title, path in main_pages:
            mermaid.append(f'    {node_id}["{title}"]')

        mermaid.append("")
        mermaid.append("    %% Section Pages")
        for node_id, title, path in section_pages:
            mermaid.append(f'    {node_id}["{title}"]')

        mermaid.append("")
        mermaid.append("    %% Resource Pages")
        for node_id, title, path in resource_pages:
            # Use shorter labels for resource pages
            short_title = title[:20] + "..." if len(title) > 20 else title
            mermaid.append(f'    {node_id}["{short_title}"]')

        mermaid.append("")

        # Create hierarchical links with subgraphs
        mermaid.append("    %% Main Navigation")
        readme_id = node_ids.get("README.md")
        if readme_id:
            for section_id, _, _ in section_pages:
                if section_id != readme_id:
                    mermaid.append(f"    {readme_id} --> {section_id}")

        mermaid.append("")
        mermaid.append("    %% Section to Resource Links")

        # Group resource links by section
        section_resources = {}
        for source_path, target_paths in self.links.items():
            if (
                source_path in node_ids
                and self.get_page_category(source_path) == "section"
            ):
                source_id = node_ids[source_path]
                for target_path in target_paths:
                    if (
                        target_path in node_ids
                        and self.get_page_category(target_path) == "resource"
                    ):
                        target_id = node_ids[target_path]
                        if source_id not in section_resources:
                            section_resources[source_id] = []
                        section_resources[source_id].append(target_id)

        # Add section to resource links
        for source_id, target_ids in section_resources.items():
            for target_id in target_ids[:5]:  # Limit to 5 links per section
                mermaid.append(f"    {source_id} --> {target_id}")

        mermaid.append("")

        # Add limited external links only for main pages
        ext_counter = 0
        for source_path, ext_links in self.external_links.items():
            if (
                source_path in node_ids
                and self.get_page_category(source_path) in ["main", "section"]
                and ext_links
            ):
                source_id = node_ids[source_path]
                for ext_link in ext_links[
                    :2
                ]:  # Limit to 2 external links per page
                    ext_id = f"EXT{ext_counter}"
                    domain = (
                        ext_link.split("/")[2]
                        if "//" in ext_link
                        else ext_link
                    )
                    domain = (
                        domain[:15] + "..." if len(domain) > 15 else domain
                    )
                    mermaid.append(f'    {ext_id}["🌐 {domain}"]')
                    mermaid.append(f"    {source_id} -.-> {ext_id}")
                    ext_counter += 1

        mermaid.append("")

        # Improved styling
        mermaid.extend(
            [
                "    %% Styling",
                "    classDef mainPage fill:#e1f5fe,stroke:#01579b,stroke-width:3px,color:#000",
                "    classDef sectionPage fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000",
                "    classDef resourcePage fill:#e8f5e8,stroke:#1b5e20,stroke-width:1px,color:#000",
                "    classDef externalLink fill:#fff3e0,stroke:#e65100,stroke-width:2px,stroke-dasharray: 5 5,color:#000",
                "",
            ]
        )

        # Apply styles
        for path, node_id in node_ids.items():
            category = self.get_page_category(path)
            if category == "main":
                mermaid.append(f"    class {node_id} mainPage")
            elif category == "section":
                mermaid.append(f"    class {node_id} sectionPage")
            else:
                mermaid.append(f"    class {node_id} resourcePage")

        # Style external links
        for i in range(ext_counter):
            mermaid.append(f"    class EXT{i} externalLink")

        return "\n".join(mermaid)

    def generate_mermaid_compact(self) -> str:
        """Generate a compact, vertical mermaid diagram showing all pages"""
        mermaid = ["flowchart TD"]

        # Create node definitions with shorter labels for better readability
        node_ids = {}
        counter = 0

        # Main page
        if "README.md" in self.pages:
            main_id = f"N{counter}"
            node_ids["README.md"] = main_id
            mermaid.append(f'    {main_id}["🏠 Home"]')
            counter += 1

        mermaid.append("")

        # Section pages
        section_pages = []
        for path, page in self.pages.items():
            if (
                path != "README.md"
                and self.get_page_category(path) == "section"
            ):
                node_id = f"N{counter}"
                node_ids[path] = node_id
                title = page["title"]
                # Add appropriate icons
                icon = (
                    "📚"
                    if "student" in path.lower()
                    else "👥"
                    if "mentor" in path.lower()
                    else "📋"
                    if "project" in path.lower()
                    else "❓"
                )
                short_title = title[:25] + "..." if len(title) > 25 else title
                mermaid.append(f'    {node_id}["{icon} {short_title}"]')
                section_pages.append((path, node_id))
                counter += 1

        mermaid.append("")

        # Resource pages organized by directory
        directories = {}
        for path, page in self.pages.items():
            if self.get_page_category(path) == "resource":
                dir_name = path.split("/")[0]
                if dir_name not in directories:
                    directories[dir_name] = []
                directories[dir_name].append((path, page))

        # Add resource pages grouped by directory
        for dir_name in sorted(directories.keys()):
            mermaid.append(f"    %% {dir_name.title()} Directory")
            for path, page in directories[dir_name]:
                node_id = f"N{counter}"
                node_ids[path] = node_id
                title = page["title"]
                # Shorten titles for resources
                short_title = title[:20] + "..." if len(title) > 20 else title
                # Add directory-specific icons
                icon = (
                    "📝"
                    if "template" in dir_name
                    else "📋"
                    if "rubric" in dir_name
                    else "🛠️"
                    if "tutorial" in dir_name
                    else "📚"
                    if "syllabus" in dir_name
                    else "👥"
                    if "mentor" in dir_name
                    else "⚙️"
                )
                mermaid.append(f'    {node_id}["{icon} {short_title}"]')
                counter += 1
            mermaid.append("")

        # Create hierarchical links
        mermaid.append("    %% Main Navigation")
        main_id = node_ids.get("README.md")
        if main_id:
            for path, node_id in section_pages:
                mermaid.append(f"    {main_id} --> {node_id}")

        mermaid.append("")
        mermaid.append("    %% Section to Resource Links")

        # Connect sections to their related resources
        for section_path, section_id in section_pages:
            section_dir = section_path.replace(".md", "")
            connected_resources = []

            # Find resources directly linked from this section
            for target_path in self.links.get(section_path, []):
                if (
                    target_path in node_ids
                    and self.get_page_category(target_path) == "resource"
                ):
                    target_id = node_ids[target_path]
                    mermaid.append(f"    {section_id} --> {target_id}")
                    connected_resources.append(target_path)

            # Also connect to resources in related directories (limit to avoid clutter)
            related_dirs = []
            if "student" in section_path.lower():
                related_dirs = [
                    "templates",
                    "rubrics",
                    "tutorials",
                    "syllabus",
                    "students",
                ]
            elif "mentor" in section_path.lower():
                related_dirs = ["mentor-ta", "templates"]
            elif "project" in section_path.lower():
                related_dirs = ["projects"]

            for dir_name in related_dirs:
                if dir_name in directories:
                    # Connect to first few items in each related directory
                    for path, _ in directories[dir_name][:3]:
                        if (
                            path in node_ids
                            and path not in connected_resources
                        ):
                            target_id = node_ids[path]
                            mermaid.append(
                                f"    {section_id} -.-> {target_id}"
                            )

        mermaid.append("")

        # Styling
        mermaid.extend(
            [
                "    %% Styling",
                "    classDef mainPage fill:#e1f5fe,stroke:#01579b,stroke-width:3px,color:#000",
                "    classDef sectionPage fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000",
                "    classDef resourcePage fill:#e8f5e8,stroke:#1b5e20,stroke-width:1px,color:#000",
                "",
            ]
        )

        # Apply styles
        for path, node_id in node_ids.items():
            category = self.get_page_category(path)
            if category == "main":
                mermaid.append(f"    class {node_id} mainPage")
            elif category == "section":
                mermaid.append(f"    class {node_id} sectionPage")
            else:
                mermaid.append(f"    class {node_id} resourcePage")

        return "\n".join(mermaid)

    def generate_graphviz(self, output_path: str = None) -> str:
        """Generate Graphviz diagram with hierarchical layout"""
        if not HAS_GRAPHVIZ:
            return "Error: Graphviz not installed. Run: pip install graphviz"

        # Create a new directed graph
        dot = graphviz.Digraph(comment="Jekyll Site Map")
        dot.attr(rankdir="TB", size="12,16", dpi="300")
        dot.attr(
            "node",
            shape="box",
            style="filled",
            fontsize="10",
            fontname="Arial",
        )

        # Define node attributes by category
        main_attrs = {
            "fillcolor": "#e1f5fe",
            "color": "#01579b",
            "penwidth": "3",
        }
        section_attrs = {
            "fillcolor": "#f3e5f5",
            "color": "#4a148c",
            "penwidth": "2",
        }
        resource_attrs = {
            "fillcolor": "#e8f5e8",
            "color": "#1b5e20",
            "penwidth": "1",
        }

        # Add nodes
        for path, page in self.pages.items():
            title = page["title"]
            label = f"{title}\n({path})"
            category = self.get_page_category(path)

            if category == "main":
                dot.node(path, label, **main_attrs)
            elif category == "section":
                dot.node(path, label, **section_attrs)
            else:
                # Shorten resource labels
                short_title = title[:30] + "..." if len(title) > 30 else title
                short_label = f"{short_title}\n({path.split('/')[-1]})"
                dot.node(path, short_label, **resource_attrs)

        # Add edges with different styles
        for source_path, target_paths in self.links.items():
            for target_path in target_paths:
                if target_path in self.pages:
                    # Use different edge styles based on relationship
                    if self.get_page_category(source_path) == "main":
                        dot.edge(
                            source_path,
                            target_path,
                            penwidth="2",
                            color="blue",
                        )
                    elif self.get_page_category(source_path) == "section":
                        dot.edge(
                            source_path,
                            target_path,
                            penwidth="1",
                            color="purple",
                        )
                    else:
                        dot.edge(
                            source_path,
                            target_path,
                            penwidth="1",
                            color="gray",
                        )

        # Group nodes by directory for better layout
        directories = {}
        for path in self.pages:
            if "/" in path:
                dir_name = path.split("/")[0]
                if dir_name not in directories:
                    directories[dir_name] = []
                directories[dir_name].append(path)

        # Create subgraphs for each directory
        for dir_name, paths in directories.items():
            with dot.subgraph(name=f"cluster_{dir_name}") as sub:
                sub.attr(
                    label=dir_name.title(),
                    style="rounded,filled",
                    fillcolor="lightgray",
                    fontsize="12",
                    fontname="Arial Bold",
                )
                for path in paths:
                    # Node already added above, just grouping
                    pass

        # Render to file if output_path provided
        if output_path:
            base_name = str(Path(output_path).with_suffix(""))
            dot.render(base_name, format="png", cleanup=True)
            
            # Try SVG generation with better error handling
            try:
                dot.render(base_name, format="svg", cleanup=True)
            except Exception as e:
                print(f"⚠️ SVG generation failed: {e}")
                # Try alternative SVG generation
                try:
                    svg_content = dot.pipe(format='svg', encoding='utf-8')
                    with open(f"{base_name}.svg", 'w', encoding='utf-8') as f:
                        f.write(svg_content)
                    print("✅ SVG generated using alternative method")
                except Exception as e2:
                    print(f"❌ Both SVG methods failed: {e2}")
                    
            return f"Graphviz diagrams saved as {base_name}.png and {base_name}.svg"

        return dot.source

    def generate_networkx(self, output_path: str = None) -> str:
        """Generate NetworkX diagram with hierarchical layout"""
        if not HAS_NETWORKX:
            return "Error: NetworkX/matplotlib not installed. Run: pip install networkx matplotlib"

        # Create directed graph
        G = nx.DiGraph()

        # Add nodes with attributes
        for path, page in self.pages.items():
            category = self.get_page_category(path)
            G.add_node(path, title=page["title"], category=category)

        # Add edges
        for source_path, target_paths in self.links.items():
            for target_path in target_paths:
                if target_path in self.pages:
                    G.add_edge(source_path, target_path)

        # Create hierarchical layout
        pos = self._create_hierarchical_layout(G)

        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(16, 20))

        # Draw nodes by category
        main_nodes = [
            n for n in G.nodes() if self.get_page_category(n) == "main"
        ]
        section_nodes = [
            n for n in G.nodes() if self.get_page_category(n) == "section"
        ]
        resource_nodes = [
            n for n in G.nodes() if self.get_page_category(n) == "resource"
        ]

        # Draw main nodes
        if main_nodes:
            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=main_nodes,
                node_color="#e1f5fe",
                node_size=2000,
                edgecolors="#01579b",
                linewidths=3,
                ax=ax,
            )

        # Draw section nodes
        if section_nodes:
            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=section_nodes,
                node_color="#f3e5f5",
                node_size=1500,
                edgecolors="#4a148c",
                linewidths=2,
                ax=ax,
            )

        # Draw resource nodes
        if resource_nodes:
            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=resource_nodes,
                node_color="#e8f5e8",
                node_size=800,
                edgecolors="#1b5e20",
                linewidths=1,
                ax=ax,
            )

        # Draw edges
        nx.draw_networkx_edges(
            G,
            pos,
            edge_color="gray",
            arrows=True,
            arrowsize=20,
            arrowstyle="->",
            ax=ax,
        )

        # Add labels
        labels = {}
        for node in G.nodes():
            title = self.pages[node]["title"]
            short_title = title[:20] + "..." if len(title) > 20 else title
            labels[node] = short_title

        nx.draw_networkx_labels(
            G, pos, labels, font_size=8, font_weight="bold", ax=ax
        )

        ax.set_title("Jekyll Site Map", fontsize=16, fontweight="bold", pad=20)
        ax.axis("off")

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            return f"NetworkX diagram saved as {output_path}"

        return "NetworkX diagram created (display with plt.show())"

    def _create_hierarchical_layout(self, G):
        """Create a hierarchical layout for the graph"""
        # Group nodes by category
        main_nodes = [
            n for n in G.nodes() if self.get_page_category(n) == "main"
        ]
        section_nodes = [
            n for n in G.nodes() if self.get_page_category(n) == "section"
        ]
        resource_nodes = [
            n for n in G.nodes() if self.get_page_category(n) == "resource"
        ]

        pos = {}

        # Position main nodes at top
        for i, node in enumerate(main_nodes):
            pos[node] = (i * 2, 3)

        # Position section nodes in middle
        for i, node in enumerate(section_nodes):
            pos[node] = (i * 1.5, 2)

        # Position resource nodes at bottom, grouped by directory
        directories = {}
        for node in resource_nodes:
            if "/" in node:
                dir_name = node.split("/")[0]
                if dir_name not in directories:
                    directories[dir_name] = []
                directories[dir_name].append(node)
            else:
                if "root" not in directories:
                    directories["root"] = []
                directories["root"].append(node)

        x_offset = 0
        for dir_name, nodes in directories.items():
            for i, node in enumerate(nodes):
                pos[node] = (x_offset + i * 0.8, 1 - (i % 3) * 0.3)
            x_offset += len(nodes) * 0.8 + 1

        return pos

    def generate_json(self) -> str:
        """Generate JSON representation"""
        result = {
            "pages": self.pages,
            "links": self.links,
            "external_links": self.external_links,
            "stats": {
                "total_pages": len(self.pages),
                "total_internal_links": sum(
                    len(links) for links in self.links.values()
                ),
                "total_external_links": sum(
                    len(links) for links in self.external_links.values()
                ),
            },
        }
        return json.dumps(result, indent=2)

    def generate_dot(self) -> str:
        """Generate Graphviz DOT format"""
        dot = ["digraph sitemap {"]
        dot.append("    node [shape=box, style=filled];")

        # Add nodes
        for path, page in self.pages.items():
            label = f"{page['title']}\\n{path}"
            color = "#e1f5fe" if path == "README.md" else "#f3e5f5"
            dot.append(f'    "{path}" [label="{label}", fillcolor="{color}"];')

        # Add edges
        for source, targets in self.links.items():
            for target in targets:
                if target in self.pages:
                    dot.append(f'    "{source}" -> "{target}";')

        dot.append("}")
        return "\n".join(dot)

    def find_orphans(self) -> set:
        """Find orphan pages with no incoming links"""
        all_pages = set(self.pages.keys())
        linked_pages = set()
        for targets in self.links.values():
            linked_pages.update(targets)
        # Exclude homepage from orphan detection
        return all_pages - linked_pages - {"README.md"}

    def find_dead_ends(self) -> set:
        """Find pages with no outgoing links"""
        return {page for page, links in self.links.items() if not links}

    def find_broken_links(self) -> dict:
        """Find broken internal links"""
        import os
        broken = {}
        # Define file extensions to validate existence but not track in sitemap
        non_markdown_extensions = {'.docx', '.pptx', '.pdf', '.xlsx', '.csv', '.json', '.yaml', '.yml', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.zip', '.tar', '.gz'}
        
        for source, targets in self.links.items():
            broken_targets = []
            source_path = self.root_path / source
            source_dir = source_path.parent
            for target in targets:
                is_non_markdown = any(target.lower().endswith(ext) for ext in non_markdown_extensions)
                if is_non_markdown:
                    # Resolve relative to source file's directory if needed
                    if target.startswith("./") or target.startswith("../"):
                        target_path = (source_dir / target).resolve()
                    else:
                        target_path = (self.root_path / target).resolve()
                    # Ensure the file is within the project root
                    try:
                        target_path.relative_to(self.root_path.resolve())
                    except ValueError:
                        broken_targets.append(target)
                        continue
                    if not target_path.exists():
                        broken_targets.append(target)
                else:
                    if target not in self.pages:
                        broken_targets.append(target)
            if broken_targets:
                broken[source] = broken_targets
        return broken


def main():
    parser = argparse.ArgumentParser(description="Generate Jekyll site map")
    parser.add_argument(
        "--output", "-o", default="sitemap.md", help="Output file"
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["mermaid", "graphviz", "networkx", "json", "dot"],
        default="graphviz",
        help="Output format",
    )
    parser.add_argument(
        "--layout",
        "-l",
        choices=["detailed", "compact"],
        default="detailed",
        help="Layout style",
    )
    parser.add_argument(
        "--root", "-r", default=".", help="Root directory of Jekyll site"
    )

    args = parser.parse_args()

    mapper = JekyllSiteMapper(args.root)
    mapper.analyze_site()

    # Find orphans and other issues
    orphans = mapper.find_orphans()
    dead_ends = mapper.find_dead_ends()
    broken_links = mapper.find_broken_links()

    # Print analysis results
    print(f"Site map generated: {args.output}")
    print(
        f"Found {len(mapper.pages)} pages with {sum(len(links) for links in mapper.links.values())} internal links"
    )
    print(
        f"Found {sum(len(links) for links in mapper.external_links.values())} external links"
    )

    if orphans:
        print(f"\n⚠️  ORPHAN PAGES FOUND ({len(orphans)}):")
        for orphan in sorted(orphans):
            print(f"  - {orphan}")
        print(
            "   These pages are not linked from anywhere and may be inaccessible!"
        )
    else:
        print("\n✅ No orphan pages found")

    if dead_ends:
        print(f"\n📄 DEAD-END PAGES ({len(dead_ends)}):")
        for dead_end in sorted(dead_ends):
            print(f"  - {dead_end}")
        print("   These pages don't link to any other pages")

    if broken_links:
        print(
            f"\n💥 BROKEN LINKS FOUND ({len(broken_links)} pages with broken links):"
        )
        for source, targets in broken_links.items():
            print(f"  - {source} -> {', '.join(targets)}")
        print("   These links point to non-existent files!")
    else:
        print("\n✅ No broken links found")

    if args.format == "mermaid":
        orphan_section = ""
        if orphans:
            orphan_section = f"""
## Orphan Pages Found
The following pages are not linked from anywhere and may be inaccessible:
{chr(10).join(f"- `{orphan}`" for orphan in sorted(orphans))}
"""

        dead_end_section = ""
        if dead_ends:
            dead_end_section = f"""
## Dead-End Pages
The following pages don't link to any other pages:
{chr(10).join(f"- `{dead_end}`" for dead_end in sorted(dead_ends))}
"""

        broken_link_section = ""
        if broken_links:
            broken_link_section = f"""
## Broken Links Found
The following pages have broken internal links:
{chr(10).join(f"- `{source}` -> {', '.join(f'`{target}`' for target in targets)}" for source, targets in broken_links.items())}
"""

        # Choose mermaid diagram based on layout option
        if args.layout == "compact":
            diagram = mapper.generate_mermaid_compact()
        else:
            diagram = mapper.generate_mermaid()

        content = f"""# Jekyll Site Map

This site map was automatically generated using `generate_sitemap.py`.

## Site Statistics
- Total pages: {len(mapper.pages)}
- Total internal links: {sum(len(links) for links in mapper.links.values())}
- Total external links: {sum(len(links) for links in mapper.external_links.values())}
- Orphan pages: {len(orphans)}
- Dead-end pages: {len(dead_ends)}
- Pages with broken links: {len(broken_links)}

## Site Map Diagram

```mermaid
{diagram}
```
{orphan_section}{dead_end_section}{broken_link_section}
## Page Inventory

| Page | Title | Category | Links Out | Status |
|------|-------|----------|-----------|--------|
"""
        for path, page in sorted(mapper.pages.items()):
            category = mapper.get_page_category(path)
            link_count = len(mapper.links.get(path, []))
            status = []
            if path in orphans:
                status.append("ORPHAN")
            if path in dead_ends:
                status.append("DEAD-END")
            if path in broken_links:
                status.append("BROKEN-LINKS")
            status_str = ", ".join(status) if status else "OK"
            content += f"| {path} | {page['title']} | {category} | {link_count} | {status_str} |\n"

    elif args.format == "graphviz":
        if not HAS_GRAPHVIZ:
            print("Error: Graphviz not installed. Run: pip install graphviz")
            return

        # Generate both PNG and SVG images
        base_name = str(Path(args.output).with_suffix(""))
        result = mapper.generate_graphviz(base_name)

        # Also save the DOT source
        dot_source = mapper.generate_graphviz()
        with open(f"{base_name}.dot", "w", encoding="utf-8") as f:
            f.write(dot_source)

        print(result)
        print(f"DOT source saved as {base_name}.dot")
        return

    elif args.format == "networkx":
        if not HAS_NETWORKX:
            print(
                "Error: NetworkX/matplotlib not installed. Run: pip install networkx matplotlib"
            )
            return

        # Generate PNG image
        png_path = str(Path(args.output).with_suffix(".png"))
        result = mapper.generate_networkx(png_path)
        print(result)
        return

    elif args.format == "json":
        content = mapper.generate_json()
    elif args.format == "dot":
        content = mapper.generate_dot()

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
