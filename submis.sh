#!/bin/bash

# Define the site URL
SITE_URL="https://tropicgranite.com"

# Define the submission URLs
SUBMISSION_URLS=(
    "https://www.google.com/intl/en/webmasters/sitemaps/ping?sitemap=${SITE_URL}/sitemap.xml"
    "https://www.bing.com/webmaster/ping.aspx?siteMap=${SITE_URL}/sitemap.xml"
    "https://duckduckgo.com/newsite?u=${SITE_URL}"
    "https://www.ecosia.org/add?url=${SITE_URL}"
    "https://search.yahoo.com/info/submit.html?u=${SITE_URL}"
    "https://www.youtube.com/submit_url?u=${SITE_URL}"
    "https://www.tiktok.com/submit_url?u=${SITE_URL}"
    "https://www.startpage.com/sp/submit.html?u=${SITE_URL}"
    "https://www.baidu.com/search/url_submit.html?url=${SITE_URL}"
    "https://webmaster.yandex.com/addurl.xml?url=${SITE_URL}"
    "https://searchadvisor.naver.com/url_submit?url=${SITE_URL}"
    "https://www.qwant.com/?action=add_url&url=${SITE_URL}"
    "https://search.brave.com/submit_url?u=${SITE_URL}"
    "https://www.swisscows.com/web?query=${SITE_URL}"
    "https://www.ask.com/web?q=${SITE_URL}"
    "https://search.lycos.com/web?q=${SITE_URL}"
    "https://www.seznam.cz/?q=${SITE_URL}"
    "https://archive.org/web/submitURL?url=${SITE_URL}"
    "https://www.shenma.com/submit_url?u=${SITE_URL}"
    "https://www.dogpile.com/info.dogpl/submit_url?u=${SITE_URL}"
)

# Function to submit the site to each search engine
submit_site() {
    local url=$1
    echo "Submitting to: $url"

    # Perform the HTTP request and capture the response, following redirects
    response=$(curl -s -L -o /dev/null -w "HTTP Code: %{http_code}\nResponse Time: %{time_total} seconds\nFinal URL: %{url_effective}\n" "$url")

    # Print the response details
    echo "Response for $url:"
    echo "$response"
    echo "----------------------------------------"
}

# Submit the site to each search engine
for url in "${SUBMISSION_URLS[@]}"; do
    submit_site "$url"
done

echo "Submission process completed."

