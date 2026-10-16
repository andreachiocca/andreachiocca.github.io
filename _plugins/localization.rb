# Native Jekyll page generation and Liquid helpers. No runtime translation service.
require 'json'

module Jekyll
  module AcademicLocalization
    def language
      (@context['page'] || {})['lang'] || 'en'
    end

    def t(message)
      return message if language == 'en' || message.nil?
      messages = @context.registers[:site].data.dig('i18n', language, 'ui') || {}
      messages.fetch(message.to_s.strip) { raise Jekyll::Errors::FatalException, "Missing #{language} interface translation: #{message}" }
    end

    def local_url(url)
      value = url.to_s
      return value unless language == 'it' && value.start_with?('/') && !value.start_with?('//')
      path, suffix = value.split(/(?=[?#])/, 2)
      routes = @context.registers[:site].config['academic_localized_routes'] || {}
      (routes[path] || path) + suffix.to_s
    end

    def localized_record(record, group)
      return record if language == 'en'
      override = @context.registers[:site].data.dig('i18n', language, group, record['id'])
      unless override
        Jekyll.logger.warn 'Translation missing:', "#{group}/#{record['id']}; English description retained"
        return record.merge('_translation_missing' => true)
      end
      forbidden = %w[id url doi github_url github_full_name zenodo_record_id creators startDate endDate actionStartDate actionEndDate date year institution name programme working_groups links further specifications verification_source]
      forbidden += %w[title name] if %w[outputs projects resume].include?(group)
      raise Jekyll::Errors::FatalException, "Translation overrides canonical fields: #{group}/#{record['id']}" unless (override.keys & forbidden).empty?
      record.merge(override)
    end
  end

  class LocalizedText < Liquid::Block
    def initialize(name, markup, tokens)
      super
      @key = markup.strip
    end

    def render(context)
      return super if context['page']['lang'] != 'it'
      text = context.registers[:site].data.dig('i18n', 'it', 'texts', @key)
      raise Jekyll::Errors::FatalException, "Missing Italian text: #{@key}" if text.to_s.strip.empty?
      Liquid::Template.parse(text).render!(context)
    end
  end

  class LocalizedPages < Generator
    safe true
    priority :low

    def generate(site)
      site.config['academic_localized_routes'] = {}
      enabled = site.config.fetch('academic_languages', ['home', 'research'])
      sources = site.pages + site.collections.values.flat_map(&:docs)
      sources.each do |source|
        key = source.data['translation_key']
        next unless key && enabled.include?(key)
        source.data['lang'] = 'en'
        source.data['alternates'] = { 'en' => source.url, 'it' => '/it' + source.url }
        metadata = site.data.dig('i18n', 'it', 'pages', key)
        raise Jekyll::Errors::FatalException, "Missing Italian page metadata: #{key}" unless metadata && metadata['description']
        translated = PageWithoutAFile.new(site, site.source, '/it' + source.url, source.extname == '.md' ? 'index.md' : 'index.html')
        translated.content = source.content
        translated.data = JSON.parse(JSON.generate(source.data)).merge(metadata)
        translated.data.merge!('lang' => 'it', 'permalink' => '/it' + source.url, 'section' => source.data['section'] || (source.is_a?(Document) ? 'teaching' : nil))
        if source.is_a?(Document)
          translated.data['description'] = source.data['description']
          translated.data['seo_description'] = metadata['description']
        end
        site.pages << translated
        site.config['academic_localized_routes'][source.url] = translated.url
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::AcademicLocalization)
Liquid::Template.register_tag('locale', Jekyll::LocalizedText)
