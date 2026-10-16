require 'jekyll'
require_relative '../_plugins/recent-publications'

Entry = Struct.new(:key, :type, :fields) do
  def [](field)
    fields[field]
  end
end
def record(key, **fields)
  Entry.new(key, :article, fields)
end
recency = Jekyll::PublicationRecency
today = Date.new(2026, 10, 16)
entries = [record('year-only', year: '2025'), record('march', year: '2025', month: 'mar'),
           record('october', year: '2025', month: 'October'), record('numeric', year: '2025', month: '9', day: '12'),
           record('iso', year: '2025', date: '2025-11-03'), record('current', year: '2026'),
           record('future', date: '2027-01-01'), record('accepted', year: '2026', status: 'accepted'),
           record('press', year: '2026', note: 'In press'), record('preprint', year: '2026', pubstate: 'preprint'),
           Entry.new('unpublished', :unpublished, { year: '2026' })]
expected = %w[current iso october numeric march]
raise 'Incorrect date order or publication eligibility' unless recency.recent(entries, today).map(&:key) == expected
raise 'Year fallback changed' unless recency.publication_date(record('year', year: '2025')) == Date.new(2025, 1, 1)
raise 'Invalid date fallback changed' unless recency.publication_date(record('bad', year: '2025', date: '2025-02-30')) == Date.new(2025, 1, 1)
raise 'Non-numeric year must be excluded' unless recency.publication_date(record('undated', year: 'forthcoming')).nil?
ties = [record('b', year: '2025'), record('a', year: '2025')]
raise 'Non-deterministic year ties' unless recency.recent(ties, today).map(&:key) == %w[a b]
entries << record('new', date: '2026-10-01')
raise 'New publication not reflected automatically' unless recency.recent(entries, today).first.key == 'new'
puts 'PASS: recent-publication date precision, year fallback, stable ties, unpublished/future exclusion and new-record selection'
