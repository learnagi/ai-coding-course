# Contributing Guide

## Directory Structure

```
repository/
├── README.md           # Tutorial information
├── chapter-1/          # Chapter directory
│   ├── README.md      # Chapter information
│   ├── section-1.md   # Section content
│   └── section-2.md
└── chapter-2/
    ├── README.md
    └── section-1.md
```

## File Format Requirements

### Tutorial README.md
```markdown
---
title: "Tutorial Title"
slug: "tutorial-slug"
description: "Tutorial description"
author: "Author Name"
status: "published"  # or "draft"
created_at: "2024-01-01"
updated_at: "2024-01-01"
---

# Tutorial Title

Tutorial content...
```

### Chapter README.md
```markdown
---
title: "Chapter Title"
slug: "chapter-slug"
sequence: 1
description: "Chapter description"
status: "published"  # or "draft"
---

# Chapter Title

Chapter content...
```

### Section Content (*.md)
```markdown
---
title: "Section Title"
slug: "section-slug"
sequence: 1
description: "Section description"
is_published: true  # or false
estimated_minutes: 10
---

# Section Title

Section content...
```

## Content Update Guidelines

1. **File Naming**
   - Use lowercase letters
   - Use hyphens for spaces
   - Keep names short and descriptive
   - Example: `git-basics.md`, `advanced-features.md`

2. **Content Organization**
   - Each chapter must have its own directory
   - Each directory must have a README.md
   - Sections must be .md files
   - Follow the sequence numbers for ordering

3. **Metadata Fields**
   - `title`: Display name
   - `slug`: URL-friendly identifier
   - `sequence`: Order number
   - `description`: Brief summary
   - `status/is_published`: Content visibility
   - `estimated_minutes`: Estimated reading time (sections only)

4. **Content Writing**
   - Use clear and concise language
   - Include code examples where relevant
   - Add images in the same directory
   - Reference images using relative paths
   - Keep content focused and well-structured

## Update Process

1. **Before Making Changes**
   ```bash
   # Pull latest changes
   git pull origin main
   
   # Create new branch
   git checkout -b feature/update-content
   ```

2. **Making Changes**
   - Update content following the format guidelines
   - Test content rendering locally
   - Verify all links and references

3. **Testing Changes**
   ```bash
   # Run sync command
   php artisan tutorial:sync-repository /path/to/repository
   
   # Check sync report
   cat storage/logs/tutorial-sync-*.log | tail -n 1
   ```

4. **Committing Changes**
   ```bash
   # Stage changes
   git add .
   
   # Commit with descriptive message
   git commit -m "update: [Chapter/Section] - Brief description"
   
   # Push changes
   git push origin feature/update-content
   ```

5. **Creating Pull Request**
   - Create PR on GitHub
   - Add description of changes
   - Request review if needed
   - Wait for approval

## Best Practices

1. **Content Quality**
   - Maintain consistent formatting
   - Check spelling and grammar
   - Ensure technical accuracy
   - Keep content up-to-date

2. **Collaboration**
   - Communicate changes with team
   - Review others' contributions
   - Provide constructive feedback
   - Follow project guidelines

3. **Version Control**
   - Make atomic commits
   - Write clear commit messages
   - Keep branches up to date
   - Resolve conflicts promptly

4. **Documentation**
   - Update related documentation
   - Add comments where needed
   - Document complex procedures
   - Keep README files current

## Need Help?

If you have questions or need assistance:
1. Check existing documentation
2. Review past commits and PRs
3. Contact project maintainers
4. Open an issue for discussion

Remember: Quality content helps everyone learn better! 
