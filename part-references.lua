-- Références locales à chaque grande partie, produites au rendu (HTML et PDF).
local REFERENCES_PER_PAGE = 10
-- Introduction : notices en pied de page uniquement, sans récapitulatif final.
local FOOTER_ONLY_PARTS = { ['1'] = true }

local function has_class(el, name)
  return el.classes:includes(name)
end

local function escape(text)
  return text:gsub('&', '&amp;'):gsub('<', '&lt;'):gsub('>', '&gt;'):gsub('"', '&quot;')
end

function Pandoc(doc)
  local catalog = doc.meta['part-references'] or {}
  local output = pandoc.List()
  local part, subpart, slide, numbers, used = nil, '1', nil, {}, {}

  local function entry(key)
    local ref = catalog[key]
    if not ref or not ref.short or not ref.full then
      error('Référence inconnue ou incomplète : ' .. key .. ' (short et full requis)')
    end
    return ref
  end

  local function register(key)
    entry(key)
    if not numbers[key] then
      used[#used+1] = key
      numbers[key] = #used
    end
    return numbers[key]
  end

  local function citation(keys)
    local labels, first = {}, nil
    for key in keys:gmatch('[^,%s]+') do
      if not slide or not slide.attributes.refs or
          not (',' .. slide.attributes.refs .. ','):find(',' .. key .. ',', 1, true) then
        error('Appel de référence absent du champ refs de la diapo : ' .. key)
      end
      local n = register(key)
      first = first or n
      labels[#labels+1] = tostring(n)
    end
    local label = '[' .. table.concat(labels, ',') .. ']'
    if FOOTER_ONLY_PARTS[part] then return '<span class="citation-call">' .. label .. '</span>' end
    return '<a class="citation-call" href="#/references-part-' .. part .. '-' ..
      math.ceil(first/REFERENCES_PER_PAGE) .. '">' .. label .. '</a>'
  end

  local function inline_citations(raw)
    if raw.format == 'html' then
      raw.text = raw.text:gsub('<span data%-cite="([^"]+)"></span>', citation)
      return raw
    end
  end

  local function recap()
    if FOOTER_ONLY_PARTS[part] then return end
    -- Dix entrées par page pour conserver une taille de lecture confortable.
    local pages = math.ceil(#used / REFERENCES_PER_PAGE)
    for page = 1, pages do
      local title = 'Références · Partie ' .. string.format('%02d', tonumber(part))
      if pages > 1 then title = title .. ' · ' .. page .. '/' .. pages end
      local classes = {'editorial', 'references-slide'}
      local attributes = {['data-part']=part, ['data-subpart']=subpart}
      if part == '2' or part == '3' then
        classes[#classes+1] = 'unnumbered-subpart'
        attributes['data-subpart'] = nil
      end
      output:insert(pandoc.Header(2, title, pandoc.Attr(
        'references-part-' .. part .. '-' .. page,
        classes, attributes)))
      local html = '<div class="slide-title">' .. escape(title) .. '</div><ol class="part-reference-list" start="' .. ((page-1)*REFERENCES_PER_PAGE+1) .. '">'
      for i = (page-1)*REFERENCES_PER_PAGE+1, math.min(page*REFERENCES_PER_PAGE, #used) do
        html = html .. '<li id="reference-' .. part .. '-' .. i .. '">' .. escape(pandoc.utils.stringify(entry(used[i]).full)) .. '</li>'
      end
      output:insert(pandoc.RawBlock('html', html .. '</ol>'))
    end
  end

  local function footer()
    if not slide or not slide.attributes.refs then return end
    if not part then error('Une diapo avec refs doit avoir data-part.') end
    local refs, seen = {}, {}
    for key in slide.attributes.refs:gmatch('[^,%s]+') do
      local ref = entry(key)
      if not numbers[key] then
        used[#used+1] = key
        numbers[key] = #used
      end
      if not seen[key] then
        local n = numbers[key]
        local page = math.ceil(n/REFERENCES_PER_PAGE)
        local text = '[' .. n .. '] ' .. escape(pandoc.utils.stringify(ref.full))
        if FOOTER_ONLY_PARTS[part] then
          refs[#refs+1] = '<span class="slide-reference-entry">' .. text .. '</span>'
        else
          refs[#refs+1] = '<a class="slide-reference-entry" href="#/references-part-' .. part .. '-' .. page .. '">' .. text .. '</a>'
        end
        seen[key] = true
      end
    end
    if #refs > 0 then
      slide.classes:insert('has-slide-references')
      output:insert(pandoc.RawBlock('html', '<div class="slide-references" role="note" aria-label="Références de la diapositive">' .. table.concat(refs, '\n') .. '</div>'))
    end
  end

  for _, block in ipairs(doc.blocks) do
    if block.t == 'Header' and block.level == 2 then
      footer()
      local next_part = block.attributes['data-part']
      if next_part ~= part or has_class(block, 'end-slide') then
        if part then recap() end
        part, numbers, used = next_part, {}, {}
      end
      subpart = block.attributes['data-subpart'] or '1'
      slide = block
      if slide.attributes.refs then
        for key in slide.attributes.refs:gmatch('[^,%s]+') do register(key) end
      end
    end
    block = block:walk({
      RawBlock=inline_citations,
      RawInline=inline_citations,
      Span=function(span)
        local keys = span.attributes['data-cite']
        if keys then return pandoc.RawInline('html', citation(keys)) end
      end
    })
    if block.t == 'Header' and block.level == 2 then slide = block end
    output:insert(block)
  end
  footer()
  if part then recap() end
  doc.blocks = output
  return doc
end
