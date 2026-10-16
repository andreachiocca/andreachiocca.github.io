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
