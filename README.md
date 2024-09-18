# Logdetective Taxonomy

This repo contains taxonomy for [Instructlab](https://github.com/instructlab) generated from data we collected on our website: https://logdetective.com/

We now have only a single file,
[knowledge/technology/qna.yaml](/knowledge/technology/qna.yaml). The file is
generated using the script
[scripts/compile_ilab_qa.py](/scripts/compile_ilab_qa.py).
Instructlab requires every knowledge to have at least 5 seed examples and every example needs at least 3 question/answer pairs.

You can read more about the syntax of the taxonomy yaml files here:
1. https://github.com/instructlab/taxonomy?tab=readme-ov-file#getting-started-with-knowledge-contributions
2. https://docs.redhat.com/en/documentation/red_hat_enterprise_linux_ai/1.1/html/creating_a_custom_llm_using_rhel_ai/customize_taxonomy_tree#customize_llm_knowledge_example

Please note that instructlab in versions 0.17 and 0.18 is strict about the
formatting and enforces line length, blank lines. There is also a change in the
schema, where ilab 0.18 enforces version 3 of the document.
