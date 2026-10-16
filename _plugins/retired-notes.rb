# Preserve old bookmarks without publishing the retired Notes catalogue or articles.
module Jekyll
  class RetiredNotesRedirects < Generator
    safe true
    priority :low

    def generate(site)
      site.data.fetch('retired_notes_urls', []).each do |url|
        filename = url.end_with?('/') ? 'index.html' : File.basename(url)
        directory = url.end_with?('/') ? url : File.dirname(url)
        page = PageWithoutAFile.new(site, site.source, directory, filename)
        page.data.merge!('layout' => 'retired-notes', 'permalink' => url,
                         'sitemap' => false, 'redirect_to' => '/research/')
        site.pages << page
      end
    end
  end
end
