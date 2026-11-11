"""Scopes a prototype's CSS under one wrapper class (same rules as extract_css.py); shared by build_home / build_category.

  :root / body             -> .kh                     (the design tokens and base text styles)
  html[...] .x             -> html[...] :where(.kh) .x
  .motion .x / .no-motion  -> .kh.motion .x           (the script puts the motion class on the wrapper)
  html.x body              -> left alone              (the page itself, e.g. no scrolling during the intro)
  .x                       -> :where(.kh) .x
"""
import re


def make(sc):
    def scope_sel(sel):
        sel = sel.strip()
        if not sel or sel.startswith(('from', 'to')) or re.fullmatch(r'[\d.]+%(\s*,\s*[\d.]+%)*', sel):
            return sel
        if re.match(r'^html[^ ]* body$', sel):
            return sel
        m = re.match(r'^\.(motion|no-motion) (.*)$', sel)
        if m:
            return f'{sc}.{m.group(1)} {m.group(2)}'
        m = re.match(r'^(html(?:\[[^\]]*\]|\.[\w-]+|:not\([^)]*\))*|:root)(.*)$', sel)
        if m:
            root, rest = m.group(1), m.group(2).strip()
            if root == ':root':
                return sc + (' ' + rest if rest else '')
            return f'{root} :where({sc})' + (' ' + rest if rest else '') if rest else f'{root} {sc}'
        if sel.startswith('body'):
            return sc + sel[4:]
        return f':where({sc}) ' + sel

    def scope_block(text):
        out, i, n = [], 0, len(text)
        while i < n:
            j = text.find('{', i)
            if j < 0:
                out.append(text[i:]); break
            head = text[i:j]
            depth, k = 1, j + 1
            while k < n and depth:
                if text[k] == '{': depth += 1
                elif text[k] == '}': depth -= 1
                k += 1
            body = text[j + 1:k - 1]
            h = head.strip()
            lead = head[:len(head) - len(head.lstrip())]
            # comments in front of an at-rule stay in front of it (they used to hide the at-rule from the checks below)
            cm0 = re.match(r'^((?:\s*/\*.*?\*/)*)\s*(.*)$', h, re.S)
            pre0, at = cm0.group(1), cm0.group(2)
            if at.startswith(('@media', '@supports', '@layer')):
                out.append(f'{lead}{pre0}{at}{{{scope_block(body)}}}')
            elif at.startswith(('@keyframes', '@font-face', '@property')):
                out.append(f'{lead}{pre0}{at}{{{body}}}')
            else:
                cm = re.match(r'^((?:\s*/\*.*?\*/)*)(.*)$', h, re.S)
                pre, sels = cm.group(1), cm.group(2)
                parts = [scope_sel(s) for s in re.split(r',(?![^(]*\))', sels)]
                out.append(f'{lead}{pre}{", ".join(parts)}{{{body}}}')
            i = k
        return ''.join(out)

    def scope(css, prefix):
        """scope the CSS and give its keyframes their own names (they are global)"""
        names = re.findall(r'@keyframes ([\w-]+)', css)
        out = scope_block(css)
        for nm in names:
            out = re.sub(rf'(@keyframes |animation:[^;{{}}]*?\b){nm}\b', rf'\1{prefix}-{nm}', out)
        return out
    return scope
