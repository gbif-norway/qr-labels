#!/usr/bin/ruby
# encoding: utf-8

require 'prawn'
require 'cgi'

PAGES = 5
COLS = 4
ROWS = 6

PREFIX = "http://purl.org/nhmuio/lid/"

query = CGI.parse(ENV['QUERY_STRING'])

pdf = Prawn::Document.new(:page_size => 'A4')
pdf.define_grid(:columns => COLS, :rows => ROWS, :column_gutter => 64, :row_gutter => 8)

pmo = (query['fra'][0] .. query['til'][0]).to_a

all = []

PAGES.times do |n|
  COLS.times do |col|
    ROWS.times.each do |row|
      next if pmo.empty?

      code = `uuidgen`.strip
      `/usr/bin/qrencode -s 4 -l M -o /tmp/#{code}.png "#{PREFIX}#{code}"`
      box = pdf.grid(row, col)
      pdf.font_size 6
      pdf.stroke_color "cccccc"

      p = pmo.shift

      pdf.bounding_box(box.top_left, :width => box.width, :height => box.height) do
        pdf.stroke_bounds if query.has_key? "grid"
        pdf.text "\n#{query['text'][0]}", :align => :center, :style => :bold
        pdf.image "/tmp/#{code}.png", :fit => [box.width, box.height]
        pdf.text "University of Oslo #{Time.now.year}\n\n", :align => :center
        pdf.text p, :align => :right, :rotate => 90
      end
      all << [p, code]
    end
  end
  pdf.start_new_page unless n == (PAGES - 1) or pmo.empty?
end

pdf.start_new_page
pdf.font("Courier") do
  all.each do |x, y|
    pdf.text "#{x}\t\t\t#{y}\t\t\t#{PREFIX}#{y}"
  end
end


`rm /tmp/*.png`

puts "Content-Type: application/pdf\n\n"
puts pdf.render

