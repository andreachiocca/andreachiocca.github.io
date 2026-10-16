require 'date'
require 'jekyll/scholar'

module Jekyll
  module PublicationRecency
    module_function

    def value(entry, field)
      entry[field].to_s.delete('{}"').strip
    end

    # Missing month/day is a sorting convention, never additional published metadata.
    def publication_date(entry)
      raw = value(entry, :date)
      if raw.match?(/\A\d{4}(-\d{2}){0,2}\z/)
        parts = raw.split('-').map(&:to_i)
        begin
          return Date.new(parts[0], parts[1] || 1, parts[2] || 1)
        rescue Date::Error
          # Fall back to the separate bibliographic year/month/day fields.
        end
      end
      year = value(entry, :year)
      return nil unless year.match?(/\A\d{4}\z/)

      month_text = value(entry, :month).downcase
      month = month_text.match?(/\A\d{1,2}\z/) ? month_text.to_i : Date::MONTHNAMES.index { |name| name && name.downcase.start_with?(month_text) }
      month = 1 if month_text.empty? || !month || !month.between?(1, 12)
      day = value(entry, :day).to_i
      Date.new(year.to_i, month, day.positive? ? day : 1)
    rescue Date::Error
      Date.new(year.to_i, 1, 1)
    end

    def recent(entries, today)
      entries.filter_map do |entry|
        next if entry.type.to_s == 'unpublished'
        state = [:status, :pubstate, :note].map { |field| value(entry, field) }.join(' ')
        next if state.match?(/\b(submitted|accepted|in[ -]?press|forthcoming|preprint|unpublished)\b/i)
        date = publication_date(entry)
        next unless date && date <= today
        [entry, date]
      end.sort_by { |entry, date| [-date.jd, entry.key.to_s] }.first(5).map(&:first)
    end
  end

  # Reuse Scholar's bibliography cache, dependency tracking and existing bib layout.
  class RecentPublicationsTag < Scholar::BibliographyTag
    def render(context)
      set_context_to context
      update_dependency_tree
      today = context.registers[:site].time.to_date
      render_items(PublicationRecency.recent(cited_entries, today))
    end
  end
end

Liquid::Template.register_tag('recent_publications', Jekyll::RecentPublicationsTag)
