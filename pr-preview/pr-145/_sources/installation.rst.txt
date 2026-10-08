Installation
============

``opinionated_mixins`` is a library. Add it to your project as a dependency.

Stable release
--------------

To add ``opinionated_mixins`` to your project, run this command in your
terminal:

.. code-block:: sh

   uv add opinionated-mixins

Or if you prefer to use ``pip``:

.. code-block:: sh

   pip install opinionated-mixins

Verify release provenance
-------------------------

Public-repository release distributions include Sigstore-signed build
provenance. After downloading a wheel or source distribution, verify that the
release workflow built it from ``main`` in this repository:

.. code-block:: sh

   gh attestation verify <downloaded-distribution> \
     --repo hasansezertasan/opinionated-mixins \
     --signer-workflow hasansezertasan/opinionated-mixins/.github/workflows/release.yml \
     --source-ref refs/heads/main

Artifact attestations are available for public repositories on current GitHub
plans. Private and internal repositories require GitHub Enterprise Cloud and
the repository variable ``ENABLE_PRIVATE_ATTESTATIONS=true``.

From source
-----------

The source files for ``opinionated_mixins`` can be downloaded from the
`GitHub repo <https://github.com/hasansezertasan/opinionated-mixins>`_.

You can either clone the public repository:

.. code-block:: sh

   git clone https://github.com/hasansezertasan/opinionated-mixins.git

Or download the
`tarball <https://github.com/hasansezertasan/opinionated-mixins/tarball/main>`_:

.. code-block:: sh

   mkdir opinionated-mixins
   curl -fL https://github.com/hasansezertasan/opinionated-mixins/tarball/main | tar -xz --strip-components=1 -C opinionated-mixins

Once you have a copy of the source, you can install it with:

.. code-block:: sh

   cd opinionated-mixins
   uv pip install .
