require 'jekyll'
require 'ostruct'
require_relative '../_plugins/localization'

site = OpenStruct.new(data: { 'i18n' => { 'it' => { 'ui' => { 'Research' => 'Ricerca' }, 'outputs' => { 'one' => { 'description' => 'Descrizione' } } } } }, config: { 'academic_localized_routes' => { '/' => '/it/', '/research/' => '/it/research/' } })
filters = Object.new.extend(Jekyll::AcademicLocalization)
context = Liquid::Context.new({ 'page' => { 'lang' => 'it' } }, {}, { site: site })
filters.instance_variable_set(:@context, context)
raise 'Translation failed' unless filters.t('Research') == 'Ricerca'
raise 'Page URL failed' unless filters.local_url('/research/#topic') == '/it/research/#topic'
%w[/assets/img/photo.jpg /TeachingMaterial/slides.pdf https://doi.org/10.1234/test mailto:test@example.org #topic].each do |url|
  raise "Rewrote #{url}" unless filters.local_url(url) == url
end
record = { 'id' => 'one', 'title' => 'Official title', 'doi' => '10.1234/test', 'description' => 'Description' }
translated = filters.localized_record(record, 'outputs')
raise 'Canonical metadata changed' unless translated['title'] == record['title'] && translated['doi'] == record['doi'] && record['description'] == 'Description'
raise 'Description not localized' unless translated['description'] == 'Descrizione'
puts 'PASS: localized labels, page links, immutable scientific data and shared asset/external URLs'

# A new translated record falls back explicitly without mutating the snapshot.
missing = filters.localized_record({ 'id' => 'new', 'description' => 'English description' }, 'outputs')
raise 'Missing translation fallback failed' unless missing['_translation_missing'] && missing['description'] == 'English description'
site.data['i18n']['it']['outputs']['one']['doi'] = 'changed'
begin
  filters.localized_record(record, 'outputs')
  raise 'Allowed an identifier override'
rescue Jekyll::Errors::FatalException
  # Expected: translations cannot change canonical scientific identifiers.
end

# Preserve Markdown conversion, public URLs and shared canonical page content.
require 'tmpdir'
Dir.mktmpdir('academic-localization') do |directory|
  config = Jekyll.configuration('source' => directory, 'destination' => File.join(directory, '_site'), 'academic_languages' => ['research'])
  fixture = Jekyll::Site.new(config)
  fixture.data['i18n'] = { 'it' => { 'pages' => { 'research' => { 'title' => 'Ricerca', 'description' => 'Descrizione' } }, 'texts' => { 'pilot' => 'Una **prova**.' } } }
  page = Jekyll::PageWithoutAFile.new(fixture, directory, '/research/', 'index.md')
  page.data.merge!('translation_key' => 'research', 'permalink' => '/research/')
  page.content = '{% locale pilot %}A **test**.{% endlocale %}'
  fixture.pages << page
  Jekyll::LocalizedPages.new.generate(fixture)
  italian = fixture.pages.find { |item| item.data['lang'] == 'it' }
  raise 'English route changed' unless page.url == '/research/'
  raise 'Wrong localized route or converter' unless italian.url == '/it/research/' && italian.extname == '.md'
  rendered = Liquid::Template.parse(italian.content).render!({ 'page' => italian.data }, registers: { site: fixture })
  html = fixture.find_converter_instance(Jekyll::Converters::Markdown).convert(rendered)
  raise 'Literal Markdown in translated output' unless html.include?('<strong>prova</strong>')
  raise 'Missing reciprocal pair' unless italian.data['alternates'] == page.data['alternates']
end
puts 'PASS: missing-description fallback, immutable identifiers, Markdown conversion and generated page pairs'
