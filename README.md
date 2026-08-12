# AI Hive Agent Skills

[![skills.sh](https://skills.sh/b/wubin1836/ai-hive-agent-skills)](https://skills.sh/wubin1836/ai-hive-agent-skills/seedance-video-edit)

233 production-oriented Agent Skills for AI image and video generation through the AI Hive OpenAPI. The collection exposes both model-level skills and focused model × capability × commercial-use-case skills so agents can select a precise workflow.

## Install

```bash
# Browse every skill in this repository
npx skills add wubin1836/ai-hive-agent-skills --list

# Install one skill
npx skills add wubin1836/ai-hive-agent-skills --skill seedance-video-edit

# Install all skills
npx skills add wubin1836/ai-hive-agent-skills --all
```

## What is included

- Seedance, Seedance 2.5, and Seedance 2.0 video skills
- MiniMax H3 video skills
- Happy Horse video skills, including video editing
- GPT Image 2 / Image2 image skills
- Nano Banana, Nano Banana 2, and Nano Banana Pro image skills
- Seedream 5.0 Lite image skills
- Text-to-video, image-to-video, reference-to-video, video editing, and video extension workflows
- E-commerce, product-detail-page, advertising, TVC, social commerce, seeding, short drama, motion comic, and storyboard workflows

See [SKILLS.md](SKILLS.md) for the complete directory.

## Requirements

- Python 3
- `requests` (`pip3 install requests`)
- An AI Hive API key in `AI_HIVE_API_KEY`, `~/.ai-hive/config.json`, or `--api-key`

The scripts query live model configuration and pricing before submitting a task. Never commit a real API key.

## Publishing

This repository follows the Agent Skills layout under `skills/*/SKILL.md` and is designed for:

```bash
gh skill publish --dry-run
gh skill publish --tag v1.0.0
```

## License

MIT. Model names and trademarks belong to their respective owners. AI Hive is an independent API platform and this repository does not claim ownership of third-party model brands.
