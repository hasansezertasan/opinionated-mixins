# Architecture

This document provides an overview of the architecture and design decisions of the opinionated-mixins project.

## Overview

The opinionated-mixins project is designed to provide reusable mixins for various Python frameworks, allowing developers to easily add common functionality to their models without duplicating code.

## Core Components

### 1. Mixins

- **PersonMixin**: A basic mixin for representing a person with common fields like name, email, and address.
- **Future Mixins**: Additional mixins for common functionality like timestamps, auditing, and soft deletion.

### 2. Framework Support

- The project supports multiple frameworks, including:
  - Pydantic
  - SQLAlchemy
  - MongoEngine
  - ODMantic
  - Beanie
  - Tortoise
  - WTForms
  - Dataclasses

### 3. Example Projects

- Example projects demonstrate how to use the mixins with different frameworks and admin panels.

## Design Decisions

### 1. Mixin Design

- Mixins are designed to be framework-agnostic where possible, allowing for easy integration with different frameworks.
- Each mixin is documented with clear examples and usage instructions.

### 2. Testing Strategy

- Unit tests for each mixin and framework.
- Integration tests to ensure compatibility with different frameworks.

### 3. Documentation

- Comprehensive documentation for each mixin, including examples and edge cases.
- Automatic API documentation using Sphinx or MkDocs.

## Future Considerations

### Community Feedback

- Gather feedback from the community to guide future development.
- Consider user suggestions for new mixins and features.
