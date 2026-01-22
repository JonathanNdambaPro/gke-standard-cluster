# Contributing to `event-driven-gcp`

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

You can contribute in many ways:

# Types of Contributions

## Report Bugs

Report bugs at https://github.com/jojo/event-driven-gcp/issues

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

## Fix Bugs

Look through the GitHub issues for bugs.
Anything tagged with "bug" and "help wanted" is open to whoever wants to implement a fix for it.

## Implement Features

Look through the GitHub issues for features.
Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

## Write Documentation

event-driven-gcp could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

## Submit Feedback

The best way to send feedback is to file an issue at https://github.com/jojo/event-driven-gcp/issues.

If you are proposing a new feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

# Get Started!

Ready to contribute? Here's how to set up `event-driven-gcp` for local development.
Please note this documentation assumes you already have `uv` and `Git` installed and ready to go.

1. Fork the `event-driven-gcp` repo on GitHub.

2. Clone your fork locally:

```bash
cd <directory_in_which_repo_should_be_created>
git clone git@github.com:YOUR_NAME/event-driven-gcp.git

```

3. Now we need to install the environment. Navigate into the directory

```bash
cd event-driven-gcp

```

Then, install and activate the environment with:

```bash
uv sync

```

4. Install pre-commit to run linters/formatters at commit time:

```bash
uv run pre-commit install

```

5. Create a branch for local development:

```bash
git checkout -b name-of-your-bugfix-or-feature

```

Now you can make your changes locally.

6. Don't forget to add test cases for your added functionality to the `tests` directory.
7. When you're done making changes, check that your changes pass the formatting tests.

```bash
make check

```

Now, validate that all unit tests are passing:

```bash
make test

```

9. Before raising a pull request you should also run tox.
This will run the tests across different versions of Python:

```bash
tox

```

This requires you to have multiple versions of python installed.
This step is also triggered in the CI/CD pipeline, so you could also choose to skip this step locally.

10. Commit your changes and push your branch to GitHub.
**Please follow the [Commit Message Guidelines](https://www.google.com/search?q=%23commit-message-guidelines) below.**

```bash
git add .
git commit -m "feat: add new handler for pubsub events"
git push origin name-of-your-bugfix-or-feature

```

11. Submit a pull request through the GitHub website.

# Commit Message Guidelines

We follow the **[Conventional Commits](https://www.google.com/search?q=https://www.conventionalcommits.org/)** specification. This leads to more readable messages that are easy to follow when looking through the project history.

Each commit message consists of a **header**, a **body**, and a **footer**. The header has a special format that includes a **type**, a **scope**, and a **subject**:

```text
<type>(<scope>): <subject>

```

### Allowed Types

| Type | Description |
| --- | --- |
| **feat** | A new feature (corresponds to `MINOR` in SemVer). |
| **fix** | A bug fix (corresponds to `PATCH` in SemVer). |
| **docs** | Documentation only changes. |
| **style** | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc). |
| **refactor** | A code change that neither fixes a bug nor adds a feature. |
| **perf** | A code change that improves performance. |
| **test** | Adding missing tests or correcting existing tests. |
| **build** | Changes that affect the build system or external dependencies (example scopes: `pip`, `uv`, `docker`). |
| **ci** | Changes to our CI configuration files and scripts (example scopes: `github-actions`). |
| **chore** | Other changes that don't modify `src` or `test` files. |
| **revert** | Reverts a previous commit. |

### Breaking Changes

If your change breaks backward compatibility (e.g., removing a public API method), you must indicate it to trigger a `MAJOR` version update. You can do this by:

1. Adding an `!` after the type: `feat!: drop support for python 3.9`
2. Or adding a footer: `BREAKING CHANGE: The 'auth' parameter is no longer accepted.`

# Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated.
Put your new functionality into a function with a docstring, and add the feature to the list in `README.md`.
3. Ensure your commit messages follow the Conventional Commits specification described above.

```
