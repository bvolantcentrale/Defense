-- Références locales à chaque grande partie, produites au rendu (HTML et PDF).
local function has_class(el, name)
  return el.classes:includes(name)
end

local function escape(text)
  return text:gsub('&', '&amp;'):gsub('<', '&lt;'):gsub('>', '&gt;'):gsub('"', '&quot;')
end

function Pandoc(doc)
  local catalog = doc.meta['part-references'] or {}
  local output = pandoc.List()
  local part, slide, numbers, used = nil, nil, {}, {}

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
    local labels = {}
    for key in keys:gmatch('[^,%s]+') do
      if not slide or not slide.attributes.refs or
          not (',' .. slide.attributes.refs .. ','):find(',' .. key .. ',', 1, true) then
        error('Appel de référence absent du champ refs de la diapo : ' .. key)
      end
      local n = register(key)
      labels[#labels+1] = tostring(n)
    end
    local label = '[' .. table.concat(labels, ',') .. ']'
    return '<span class="citation-call">' .. label .. '</span>'
  end

  local function inline_citations(raw)
    if raw.format == 'html' then
      raw.text = raw.text:gsub('<span data%-cite="([^"]+)"></span>', citation)
      return raw
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
        local text = '[' .. n .. '] ' .. escape(pandoc.utils.stringify(ref.full))
        refs[#refs+1] = '<span class="slide-reference-entry">' .. text .. '</span>'
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
        part, numbers, used = next_part, {}, {}
      end
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
  doc.blocks = output
  return doc
end
