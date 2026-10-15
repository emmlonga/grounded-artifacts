# Third-party notices

## Writing V2 (`writers/decision-artifact-writing-v2.md`)

Writing V2 is an original condensation, adapted to this workflow, of the operating model of **Better Writing** (`forjd/better-writing`, v1.3.0, commit `fc7ef059e93f7327625b4794ad7af873e63316f7`), plus one check (the relation test) from **Clarity** (`addyosmani/clarity`, v0.2.1, commit `e27ceeff60368cf6966b4ea00a5b9b36418ee9a0`). Its frontmatter records this provenance. It reuses a small amount of upstream wording, mainly two example sentences. Neither upstream skill is redistributed here. Both are MIT-licensed, and their notices follow.

### Better Writing

```
MIT License

Copyright (c) 2026 Forjd

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Clarity

```
MIT License

Copyright (c) 2026 Addy Osmani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Render profile reference document (not distributed)

`profiles/build_reference_docx.py` builds `profiles/plain/reference.docx` from the default `reference.docx` that your own pandoc installation prints (`pandoc --print-default-data-file reference.docx`). It replaces that file's styles, page geometry and footer. Pandoc is copyright John MacFarlane and is released under the GNU General Public License, version 2 or later. This repository distributes the builder only, not the resulting file. Generate the file once after installing pandoc:

```bash
python3 profiles/build_reference_docx.py plain
```

The `plain` calibration in `profiles/plain/profile.md` was measured on a file built with pandoc 3.12.
