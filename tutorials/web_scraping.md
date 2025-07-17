---
title: "Web Scraping Guidelines"
---

# Web Scraping

Data Science clinic projects may require downloading or "scraping" information from a website. Examples may include using Yelp to identify restaurants and businesses in a specific area or downloading prices from Amazon. While downloading publicly available data from a website is not illegal in and of itself, there are some things that need to be considered before starting a project. The purpose of this document is to present a checklist of items to be considered before starting.

## Legal and Ethical Considerations

Before presenting the following, please note that we are not lawyers and if there is any gray area it should be discussed with your mentor. If you are interested in learning more about the specific legal considerations, [this article](https://digitalcommons.pepperdine.edu/cgi/viewcontent.cgi?article=1194&context=jbel) has quite a bit of information. 

Our primary legal concern is making sure to _not_ violate any terms of service specified by the data provider. If they explicitly state that behavior is not allowed as part of an agreement that you are expected to enter into when using the site, then do not violate the terms of that agreement. There is a notion of `fair use` which is invoked in legal proceedings against web scrapers. [Fair use](https://www.nolo.com/legal-encyclopedia/fair-use-the-four-factors.html) is _not_ an automatic get out of jail free card and only governs a specific 

Beyond the legal aspects, there are additional ethical considerations that should be verified before undertaking any web scraping project. The first four ethical considerations are taken from the aforementioned article:

1. Make sure your scraper is a good citizen of the web and does not overburden the targeted website.
2. The information copied was publicly available and not behind a password authentication barrier.
3. The information copied was primarily factual in nature, and the taking did not infringe on the rights—including copyrights—of
another.
4. The information was used to create a transformative product and was not used to steal market share from the target website by
luring away users or creating a substantially similar product.
5. Note that many websites will have a `robots.txt` file (which can usually be found at the root of a url, so if you are going to `https://some-company.com`, then navigate to `https://some-compnay.com/robots.txt`). The purpose of [robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro) is to define the rules for scraping or crawling a website. Before doing any serious scraping please consult this file as it may contain information about who and when scraping is allowed.
6. If there is an API or specific guidelines provided about accessing the data, those APIs and specific guidelines are used / respected.

If your data science clinic project involves web scraping, please ensure you adhere to the ethical guidelines outlined above. If you are not sure about any of them please ask your project mentor or the clinic administrative staff.

## Additional hints

Many organizations (especially non-profits and research groups) may have alternative methods of getting data. It's recommended to send an email to an organization to ask them if they have the data available in a way that doesn't require scrapping. 

Secondly, when dealing with government sources there is the "Freedom of Information Act" ("FOIA") a mechanism by which citizens are allowed to request information from the government. At the federal level, the FOIA process begins [here](https://www.foia.gov/). Every state in the United States has implemented their own version of this concept and getting information from this process can be surprisingly quick. If you are going to use FOIA you need to identify the agency that has the data you are interested in and the FOIA office that has domain over them. There are often online forms that you can fill out to request specific data.

## Summary

Web scraping can be an important part of a data science clinic project, but one that can easily veer into illegal or (more likely) unethical areas. Please make sure to go through the guidelines above before beginning any such project.