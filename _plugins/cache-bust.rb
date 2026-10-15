require 'digest'
require 'uri'

module Jekyll
  module CacheBust
    def bust_file_cache(file_name)
      site = @context.registers[:site]
      # Resolve the asset path even when the site is hosted below a base URL.
      path = URI.parse(file_name).path.delete_prefix(site.config['baseurl'].to_s).sub(%r{^/}, '')
      digest = Digest::SHA256.file(File.join(site.source, path)).hexdigest
      "#{file_name}?v=#{digest[0, 16]}"
    end

    def bust_css_cache(file_name)
      site = @context.registers[:site]
      sources = Dir.glob(File.join(site.source, '{_sass,assets/css}', '**', '*'))
                   .select { |path| File.file?(path) }.sort
      sources << File.join(site.source, '_config.yml')
      digest = Digest::SHA256.new
      sources.each do |path|
        digest.update(path.delete_prefix(site.source))
        digest.update(File.binread(path))
      end
      "#{file_name}?v=#{digest.hexdigest[0, 16]}"
    end
  end
end

Liquid::Template.register_filter(Jekyll::CacheBust)
