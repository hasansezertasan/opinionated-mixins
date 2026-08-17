# Copyright 2024 Hasan Sezer Taşan <hasansezertasan@gmail.com>
# Copyright (C) 2024 <hasansezertasan@gmail.com>
from .person import Person as Person
import warnings

warning_message = """
ODMantic doesn't support Models and Embedded models inheritance (Mixins) yet.
Check out [this issue](https://github.com/hasansezertasan/opinionated-mixins/issues/11)
for more information.
"""
warnings.warn(warning_message, UserWarning)
