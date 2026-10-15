require 'tmpdir'
require 'fileutils'
require 'ostruct'
require 'liquid'
require_relative '../_plugins/cache-bust'

Dir.mktmpdir do |source|
  FileUtils.mkdir_p(File.join(source, '_sass'))
  FileUtils.mkdir_p(File.join(source, 'assets/css'))
  File.write(File.join(source, '_config.yml'), 'max_width: 800px')
  sass = File.join(source, '_sass/_base.scss')
  main = File.join(source, 'assets/css/main.scss')
  File.write(sass, 'body { color: black; }')
  File.write(main, '@import "base";')
  filters = Object.new.extend(Jekyll::CacheBust)
  site = OpenStruct.new(source: source, config: { 'baseurl' => '/portfolio' })
  filters.instance_variable_set(:@context, OpenStruct.new(registers: { site: site }))
  before = filters.bust_css_cache('/portfolio/assets/css/main.css')
  raise 'Fingerprint is unstable' unless before == filters.bust_css_cache('/portfolio/assets/css/main.css')
  File.write(sass, 'body { color: blue; }')
  after_sass = filters.bust_css_cache('/portfolio/assets/css/main.css')
  raise 'Sass changes did not invalidate CSS' if before == after_sass
  File.write(main, '@import "base"; body { margin: 0; }')
  raise 'Entrypoint changes did not invalidate CSS' if after_sass == filters.bust_css_cache('/portfolio/assets/css/main.css')
  raise 'Base URL asset lookup failed' unless filters.bust_file_cache('/portfolio/assets/css/main.scss').include?('?v=')
end
puts 'PASS: stable fingerprints, Sass and entrypoint invalidation, and base URL asset lookup'
