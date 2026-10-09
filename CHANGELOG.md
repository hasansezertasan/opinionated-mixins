# Changelog

## [0.1.0](https://github.com/hasansezertasan/opinionated-mixins/compare/v0.0.1...v0.1.0) (2026-10-09)


### ⚠ BREAKING CHANGES

* make NotificationMixin actor fields required ([#46](https://github.com/hasansezertasan/opinionated-mixins/issues/46))
* remove input-layer frameworks, scope to storage only ([#35](https://github.com/hasansezertasan/opinionated-mixins/issues/35))

### 🚀 Features

* add ActivityMixin for event-level activity records ([#42](https://github.com/hasansezertasan/opinionated-mixins/issues/42)) ([#45](https://github.com/hasansezertasan/opinionated-mixins/issues/45)) ([2828d50](https://github.com/hasansezertasan/opinionated-mixins/commit/2828d500b1dbefe74f57051fbf9ae12bd6371afb))
* add AGENTS.md agent guide ([#118](https://github.com/hasansezertasan/opinionated-mixins/issues/118)) ([106d374](https://github.com/hasansezertasan/opinionated-mixins/commit/106d374c7356f26453922272f1c2b9b52439bde3))
* add Feedback mixin across all contrib modules ([#26](https://github.com/hasansezertasan/opinionated-mixins/issues/26)) ([10bc2ee](https://github.com/hasansezertasan/opinionated-mixins/commit/10bc2ee538e4d7b514a36a5c9f8f79db0444b37b))
* add infrastructure mixins (CreatedAt, UpdatedAt, IsActive, IntegerID, UUIDID) ([#38](https://github.com/hasansezertasan/opinionated-mixins/issues/38)) ([68e2932](https://github.com/hasansezertasan/opinionated-mixins/commit/68e29326b3db2166762f5ee481869b1562812930))
* add Lead mixin across all contrib modules ([#28](https://github.com/hasansezertasan/opinionated-mixins/issues/28)) ([a60f36e](https://github.com/hasansezertasan/opinionated-mixins/commit/a60f36ed51043c79c012b3a1d00423ee5b2fb324))
* add NotificationMixin for per-recipient notification tracking ([#43](https://github.com/hasansezertasan/opinionated-mixins/issues/43)) ([17e6104](https://github.com/hasansezertasan/opinionated-mixins/commit/17e61041f93bd86511ddd6a5e1211eb2608c7b0f))
* add Person mixin across all contrib modules ([#25](https://github.com/hasansezertasan/opinionated-mixins/issues/25)) ([be151c1](https://github.com/hasansezertasan/opinionated-mixins/commit/be151c17e2c50298b003357a1121d19a4f85e93e))
* add Template mixin across all contrib modules ([#27](https://github.com/hasansezertasan/opinionated-mixins/issues/27)) ([a537dc4](https://github.com/hasansezertasan/opinionated-mixins/commit/a537dc477ec207fe649d50401aebf2f3b8450bac))
* add User mixin across all contrib modules ([#29](https://github.com/hasansezertasan/opinionated-mixins/issues/29)) ([c9a73d5](https://github.com/hasansezertasan/opinionated-mixins/commit/c9a73d52046b96e079fdbad0d8eeb5b507fa7ba3))
* make NotificationMixin actor fields required ([#46](https://github.com/hasansezertasan/opinionated-mixins/issues/46)) ([2f5208b](https://github.com/hasansezertasan/opinionated-mixins/commit/2f5208b6e78fc5c8473eb764c8f4e9274e89c96c))
* **rfc:** add RFC process and backfill existing mixin RFCs ([#71](https://github.com/hasansezertasan/opinionated-mixins/issues/71)) ([924ef32](https://github.com/hasansezertasan/opinionated-mixins/commit/924ef32e1fd66fa0f7d5d2dbedfec92711e7a0e6))
* **sqlalchemy:** document index recommendations instead of using index=True ([#130](https://github.com/hasansezertasan/opinionated-mixins/issues/130)) ([6ed8037](https://github.com/hasansezertasan/opinionated-mixins/commit/6ed803753fd71c97eed471f8b5e729bdc9c206b1))


### 🐛 Bug Fixes

* exclude release-please CHANGELOG.md from typos ([#159](https://github.com/hasansezertasan/opinionated-mixins/issues/159)) ([2a63ff5](https://github.com/hasansezertasan/opinionated-mixins/commit/2a63ff5f84f4a6d7605614fdb71c2ec1e26ba480))
* **odmantic:** support mixin composition ([#127](https://github.com/hasansezertasan/opinionated-mixins/issues/127)) ([4c82a64](https://github.com/hasansezertasan/opinionated-mixins/commit/4c82a645b9acfdbaf6723d60ad1c845455a4c51a))
* remove BaseModel inheritance from Pydantic mixins ([#31](https://github.com/hasansezertasan/opinionated-mixins/issues/31)) ([7ea80bf](https://github.com/hasansezertasan/opinionated-mixins/commit/7ea80bfd416d5d7747185dcf48c91eec6127963f))
* **tests:** stop odmantic mixin xfails from breaking CI under pydantic 2.13 ([#72](https://github.com/hasansezertasan/opinionated-mixins/issues/72)) ([2dcb378](https://github.com/hasansezertasan/opinionated-mixins/commit/2dcb378b4e6b3d2019f1e0fb82f70eb4de5c63e8))


### ♻️ Refactoring

* remove input-layer frameworks, scope to storage only ([#35](https://github.com/hasansezertasan/opinionated-mixins/issues/35)) ([5f7378e](https://github.com/hasansezertasan/opinionated-mixins/commit/5f7378ee79da80183ff22902281131a7df89d27e))


### 📝 Documentation

* add framework proposal issue template ([#37](https://github.com/hasansezertasan/opinionated-mixins/issues/37)) ([fe0064d](https://github.com/hasansezertasan/opinionated-mixins/commit/fe0064d0fef8fa7e7690ad78a1d242de28e3791e))
* add related project references to README ([#69](https://github.com/hasansezertasan/opinionated-mixins/issues/69)) ([76071dc](https://github.com/hasansezertasan/opinionated-mixins/commit/76071dc21ab7a3a18dbcbbb46f991006b3ae9317))
* improve project documentation and issue templates ([#23](https://github.com/hasansezertasan/opinionated-mixins/issues/23)) ([2419c2a](https://github.com/hasansezertasan/opinionated-mixins/commit/2419c2a7a82358ae514b81b1ae82adb06b7348de))
* refresh project guides and admin examples ([#95](https://github.com/hasansezertasan/opinionated-mixins/issues/95)) ([5e14760](https://github.com/hasansezertasan/opinionated-mixins/commit/5e14760772c9b83c011c5c90306f263d1b14837c))
* **rfc:** codify consensus criteria for weighing references ([#156](https://github.com/hasansezertasan/opinionated-mixins/issues/156)) ([5be7e01](https://github.com/hasansezertasan/opinionated-mixins/commit/5be7e01a112522f6a1945ae6b50555c569f7a5d0))
* **rfc:** propose Slug mixin (RFC-0014) ([#135](https://github.com/hasansezertasan/opinionated-mixins/issues/135)) ([57116ac](https://github.com/hasansezertasan/opinionated-mixins/commit/57116ac60641d2991a8c3f5c4e444e3ce06714c9))


### 🧪 Tests

* add cross-framework field consistency tests ([#33](https://github.com/hasansezertasan/opinionated-mixins/issues/33)) ([3ef635c](https://github.com/hasansezertasan/opinionated-mixins/commit/3ef635c96132dd1a84a0a3b57e58e2c25a046fe9))
* add integration tests for MongoEngine and ODMantic mixins ([#40](https://github.com/hasansezertasan/opinionated-mixins/issues/40)) ([21e1848](https://github.com/hasansezertasan/opinionated-mixins/commit/21e1848f065eea13a4e620790db214a5c643e948))


### 🛠 Build

* **deps-dev:** bump ruff from 0.15.11 to 0.15.12 ([#51](https://github.com/hasansezertasan/opinionated-mixins/issues/51)) ([d06c522](https://github.com/hasansezertasan/opinionated-mixins/commit/d06c522ba7b48af0388200e1327581b9a46b5325))
* **deps-dev:** bump ruff from 0.15.12 to 0.15.16 ([#57](https://github.com/hasansezertasan/opinionated-mixins/issues/57)) ([be9038d](https://github.com/hasansezertasan/opinionated-mixins/commit/be9038deaff12d930cd0b7bbba58d95a5c99df0d))
* **deps-dev:** bump sqlalchemy from 2.0.49 to 2.0.50 ([#54](https://github.com/hasansezertasan/opinionated-mixins/issues/54)) ([1e54cff](https://github.com/hasansezertasan/opinionated-mixins/commit/1e54cffdc7a1b2bd15cf4f3f5e83d9e98acd0345))
* **deps-dev:** update coverage requirement from &gt;=7.13.5 to &gt;=7.14.1 ([#58](https://github.com/hasansezertasan/opinionated-mixins/issues/58)) ([ea0cef0](https://github.com/hasansezertasan/opinionated-mixins/commit/ea0cef02a03cbbd5df7da0a884319b72997133e1))
* **deps-dev:** update coverage requirement from &gt;=7.14.1 to &gt;=7.14.3 ([#68](https://github.com/hasansezertasan/opinionated-mixins/issues/68)) ([8da194a](https://github.com/hasansezertasan/opinionated-mixins/commit/8da194ad103df4e3e9ef5318af80c56cb2ab5910))
* **deps-dev:** update coverage requirement from &gt;=7.14.3 to &gt;=7.15.2 ([#81](https://github.com/hasansezertasan/opinionated-mixins/issues/81)) ([a83dff1](https://github.com/hasansezertasan/opinionated-mixins/commit/a83dff15389324ebde7eb88f7ccbe3db9e29e5ac))
* **deps-dev:** update coverage requirement from &gt;=7.15.2 to &gt;=7.16.0 ([#100](https://github.com/hasansezertasan/opinionated-mixins/issues/100)) ([3cf0b9f](https://github.com/hasansezertasan/opinionated-mixins/commit/3cf0b9f844c8fc63a543a2672e7e1b7b43080d6a))
* **deps-dev:** update coverage requirement from &gt;=7.16.0 to &gt;=7.16.2 ([#112](https://github.com/hasansezertasan/opinionated-mixins/issues/112)) ([a14bb5b](https://github.com/hasansezertasan/opinionated-mixins/commit/a14bb5b4512aaa7c8e93c6996ef744948899335a))
* **deps-dev:** update mongomock-motor requirement from &gt;=0.0.32 to &gt;=0.0.36 ([#48](https://github.com/hasansezertasan/opinionated-mixins/issues/48)) ([9b8fed8](https://github.com/hasansezertasan/opinionated-mixins/commit/9b8fed81386b762153ce06bbd6d645e7a91461ae))
* **deps-dev:** update mypy requirement from &gt;=1.20.1 to &gt;=1.20.2 ([#52](https://github.com/hasansezertasan/opinionated-mixins/issues/52)) ([ded19db](https://github.com/hasansezertasan/opinionated-mixins/commit/ded19db11a6edd09572b8a32730d9aff5545078d))
* **deps-dev:** update mypy requirement from &gt;=1.20.2 to &gt;=2.1.0 ([#56](https://github.com/hasansezertasan/opinionated-mixins/issues/56)) ([1c05b4c](https://github.com/hasansezertasan/opinionated-mixins/commit/1c05b4c8f86219a0dda076617baa89bd97852628))
* **deps-dev:** update mypy requirement from &gt;=2.1.0 to &gt;=2.3.0 ([#83](https://github.com/hasansezertasan/opinionated-mixins/issues/83)) ([082d1db](https://github.com/hasansezertasan/opinionated-mixins/commit/082d1db53491eba2350efe977cbe9db217f240a5))
* **deps-dev:** update mypy requirement from &gt;=2.3.0 to &gt;=2.3.1 ([#101](https://github.com/hasansezertasan/opinionated-mixins/issues/101)) ([d5a1f19](https://github.com/hasansezertasan/opinionated-mixins/commit/d5a1f19ba37e200a6a4005e2b65cb9c1275f392d))
* **deps-dev:** update pytest-asyncio requirement from &gt;=0.26.0 to &gt;=1.3.0 ([#50](https://github.com/hasansezertasan/opinionated-mixins/issues/50)) ([9f4340b](https://github.com/hasansezertasan/opinionated-mixins/commit/9f4340bcee9481f22f53ee632aab83e2848d32f8))
* **deps-dev:** update pytest-asyncio requirement from &gt;=1.3.0 to &gt;=1.4.0 ([#55](https://github.com/hasansezertasan/opinionated-mixins/issues/55)) ([ac92f9b](https://github.com/hasansezertasan/opinionated-mixins/commit/ac92f9b373510197aac4ce497726c8334c1e6a6b))
* **deps-dev:** update testcontainers requirement from &gt;=4.10.0 to &gt;=4.14.2 ([#49](https://github.com/hasansezertasan/opinionated-mixins/issues/49)) ([49c34ee](https://github.com/hasansezertasan/opinionated-mixins/commit/49c34eee7c9a1bbb1771cb02f95d593b65910b16))
* **deps-dev:** update testcontainers requirement from &gt;=4.14.2 to &gt;=4.15.0 ([#82](https://github.com/hasansezertasan/opinionated-mixins/issues/82)) ([ca5e1e0](https://github.com/hasansezertasan/opinionated-mixins/commit/ca5e1e085682238f8a1e9ce2d2a3f938135d7d78))
* **deps:** bump actions/checkout from 6.0.2 to 6.0.3 ([#53](https://github.com/hasansezertasan/opinionated-mixins/issues/53)) ([8125a1f](https://github.com/hasansezertasan/opinionated-mixins/commit/8125a1f37155557f980d946e1388fc20d22c9f4d))
* migrate from hatch to uv and drop Python 3.8-3.9 ([#24](https://github.com/hasansezertasan/opinionated-mixins/issues/24)) ([8423101](https://github.com/hasansezertasan/opinionated-mixins/commit/84231015b31b43beb37bb06ddde75b1c672562a7))
