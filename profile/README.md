# NgTrgGiang.github.io

Personal portfolio for Nguyen Truong Giang - AI & Automation Engineer.
Single self-contained `index.html`, no build step, no external requests.

## Deploy to GitHub Pages (user site)

A user site must live in a repo named exactly `NgTrgGiang.github.io`.

```bash
# from this folder
git init                      # if not already a repo
git add index.html README.md
git commit -m "Add portfolio"

# create the repo named NgTrgGiang.github.io on GitHub, then:
git remote add origin https://github.com/NgTrgGiang/NgTrgGiang.github.io.git
git branch -M main
git push -u origin main
```

Then in the repo: **Settings -> Pages -> Build and deployment -> Source: Deploy from a branch -> `main` / `root`**.
The site goes live at `https://NgTrgGiang.github.io` within a minute or two.

> Note: this folder's current remote points at `github.com/NgTrgGiang/test.git`.
> For a project page it would live at `https://NgTrgGiang.github.io/test/` instead.

## Customize

Everything is in `index.html`:

- **Name / role / bio**: search for `Truong Giang`, the hero `h1`, and the About section.
- **Projects**: the `.bento` block. Replace the placeholder GitHub links (`https://github.com/NgTrgGiang`) with the real repo URLs.
- **Skills**: the `.skill-grid` block.
- **Contact**: the `mailto:` link and GitHub URL.
- **Accent color**: change `--accent` / `--accent-2` in the `:root` token block.
- **Add a photo**: swap the monogram `.portrait` block for an `<img>` if you want a real headshot.

## Local preview

Just open `index.html` in a browser, or:

```bash
python -m http.server 8000
# then visit http://localhost:8000
```
