---
layout: default
title: Contributing
nav_order: 9
nav_exclude: true
---

# Contributing

You are welcome to improve the documentation and examples through [Issues](https://github.com/FFTAI/fourier-grx-M4/issues) or Pull Requests. Whether you are fixing a typo, clarifying a procedure, or expanding interface documentation, please include information that allows the change to be verified.

## Reporting Issues

When opening an Issue, include where applicable:

- The URL of the documentation page or its file path in the repository.
- What is wrong or unclear in the current content, and the correction or addition you suggest.
- For robot behaviour or interface issues, the robot model, `fourier-grx` version, and run mode.
- For example code, the working directory, command used, complete error message, and development environment. Do not include passwords, tokens, or other sensitive information.

## Submitting Changes

1. Keep each change focused on a clear topic, and avoid mixing it with unrelated whole-file formatting.
2. When changing a Chinese page, update its English counterpart under `docs/en/`; when changing an example, check that the related example documentation remains accurate.
3. Verify technical content against the actual commands, configuration, and code paths. Do not present unverified assumptions as facts.
4. In the Pull Request, summarize the changes, affected pages, and checks performed. For behaviour changes, include the evidence used to verify them.

## Documentation Conventions

- Pages normally need `layout: default`, `title`, and `nav_order`. Child pages also need the correct `parent`, and parent pages need `has_children` when required by the existing navigation structure.
- Internal links and asset paths in documentation pages normally start with `/fourier-grx-M4/`; the root README uses repository-relative paths.
- When adding a task page, update the Chinese and English task tables, task indexes, and related interface mappings instead of leaving an isolated page.
- Use inline code formatting for commands, file names, interface fields, and version numbers, and keep the technical content aligned across languages.

## Pre-submission Checks

This repository does not include a standard build, test, or lint toolchain. Before submitting documentation changes, check at least that:

- New or modified internal links, images, and other asset paths are valid.
- Page front matter matches the navigation structure of the section.
- Corresponding pages under `docs/` and `docs/en/` are synchronized.
- Example commands, working directories, dependencies, and safety prerequisites are clear and consistent with the current code.

Thank you to everyone who helps improve the Fourier-GRX-M4 SDK documentation and examples.
