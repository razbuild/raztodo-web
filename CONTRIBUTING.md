# Contributing to RazTodo Web

Thanks for wanting to help with RazTodo Web. Whether you're fixing a bug, improving the Web UI, working on the API, adding tests, or improving documentation, every contribution is welcome.

RazTodo Web is a presentation layer built on top of [RazTodo](https://github.com/razbuild/raztodo). Because the two projects are developed independently, the recommended development setup keeps both repositories available locally and links them together with `uv`.

## Picking an Issue 🔎

Browse the [open issues](https://github.com/razbuild/raztodo-web/issues) and grab whatever catches your eye. Labels can give you a hint about the scope or difficulty, but don't overthink it. If something looks interesting, go for it.

If you're planning a larger change, open an issue first so we can discuss the approach before you start.

## How to Get Started 🚀

1. Pick an issue.
2. Comment on it to say you're picking it up.
3. Create a branch from the repository (fork if you don't have write access).
4. Set up the development environment.
5. Make your change.
6. Run the tests and quality checks.
7. Open a Pull Request.

> 💬 **Questions? Just ask.** If something is unclear or you're not sure where to start, open an issue or comment on an existing one. We'd rather help you get unstuck than have you guess.

## Before You Start 📝

* Check existing issues before opening a new one.
* Use the provided issue templates.
* Keep discussions respectful and constructive.
* For changes that affect the interaction between RazTodo and RazTodo Web, make sure to test both projects together.

Please follow our [Code of Conduct](https://github.com/razbuild/.github/blob/main/CODE_OF_CONDUCT.md).

## Development Setup 🛠️

RazTodo Web is developed together with the [RazTodo](https://github.com/razbuild/raztodo) core project.

You need:

* Python 3.10+
* [`uv`](https://docs.astral.sh/uv/)
* Git

### 1. Create a workspace

Create a directory for both repositories:

```bash
mkdir projects
cd projects
```

You can use any directory name you prefer.

### 2. Clone both projects

```bash
git clone https://github.com/razbuild/raztodo.git
git clone https://github.com/razbuild/raztodo-web.git
```

Your workspace should now look like:

```text
projects/
├── raztodo/
└── raztodo-web/
```

### 3. Create the integration environment

Create a third directory for the local integration environment:

```bash
mkdir raztodo-integration
cd raztodo-integration
```

Create a `pyproject.toml` file:

```toml
[project]
name = "raztodo-integration"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "raztodo",
    "raztodo-web",
]

[tool.uv.sources]
raztodo = { path = "../raztodo", editable = true }
raztodo-web = { path = "../raztodo-web", editable = true }
```

Then run:

```bash
uv sync
```

This creates an environment where both projects are installed in editable mode.

Your workspace should now look like:

```text
projects/
├── raztodo/
├── raztodo-web/
└── raztodo-integration/
    ├── .venv/
    ├── pyproject.toml
    └── uv.lock
```

### 4. Start developing

Because both packages are installed in editable mode, changes made to either repository are immediately available to the integration environment.

For example, after modifying RazTodo:

```bash
cd ../raztodo
```

you can run the Web UI using the integration environment:

```bash
cd ../raztodo-integration
uv run rt-web
```

Then open:

```text
http://127.0.0.1:8000
```

You can also use the RazTodo CLI:

```bash
uv run rt add "Test task"
uv run rt list
```

The CLI and Web UI use the same RazTodo core and database, allowing you to test the complete integration locally.

> [!TIP]
> You normally do not need to reinstall the packages after changing source code because both repositories are installed in editable mode.

## Running Tests 🧪

Run the RazTodo Web test suite from the `raztodo-web` repository:

```bash
cd ../raztodo-web
uv sync --group dev --locked
uv run pytest -v
```

Run a specific test:

```bash
uv run pytest tests/path/to/test_file.py
```

Check coverage:

```bash
uv run coverage run -m pytest
uv run coverage report -m
```

## Code Quality ✨

Before opening a PR, run:

```bash
uv run ruff format --check src tests
uv run ruff check src tests
uv run ty check src
```

To automatically format the code:

```bash
uv run ruff format src tests
```

These checks are also run by CI, so passing them locally saves a round trip.

Please add tests for new functionality and update the documentation when behavior changes.

## Working Across Both Repositories 🔗

Some changes may require modifications to both RazTodo and RazTodo Web.

For example:

```text
raztodo/
    Core / Application / CLI
             ▲
             │
             │
raztodo-web/
    FastAPI / REST API / Web UI
```

If a change modifies the interface between the two projects:

1. Make the required changes in both repositories.
2. Use the local integration environment described above.
3. Test the CLI and Web UI together.
4. Open separate PRs when changes belong to both repositories.

Keep the dependency relationship in mind: RazTodo Web depends on the public interfaces provided by RazTodo.

## Commit Messages 📨

Use conventional prefixes:

* `feat:` New features
* `fix:` Bug fixes
* `docs:` Documentation
* `test:` Tests
* `refactor:` Refactoring
* `chore:` Maintenance

Example:

```text
feat: add task filtering by project
fix: handle missing task data
docs: update API documentation
test: add task route coverage
refactor: simplify task service
```

## Branch Naming 🌿

Use clear branch names that describe the change you're making:

* `feat/` New features
* `fix/` Bug fixes
* `docs/` Documentation changes
* `test/` Test changes
* `refactor/` Code improvements without behavior changes
* `chore/` Maintenance tasks

Examples:

```text
feat/add-task-filters
fix/handle-missing-task
docs/update-api-guide
test/add-route-tests
refactor/simplify-api-handler
```

## Pull Requests 🔃

A good PR description includes:

* What problem it solves
* How it solves it
* What you tested, and how
* Screenshots or recordings for Web UI changes
* Any related documentation updates
* Whether changes to the RazTodo core are also required

Keep it short and clear. No need to over-explain.

## What Happens After I Open a PR? 👀

A maintainer will review your PR and may request changes. Update your PR based on the feedback, and it will be merged once approved.

For changes involving both RazTodo and RazTodo Web, the maintainers may coordinate the PRs across both repositories to keep the projects compatible.

## Keep Going 🔁

Merged your first PR? Grab [another issue](https://github.com/razbuild/raztodo-web/issues). You already know your way around now, we'd love to see you back.