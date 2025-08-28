# Evaluating Reasoning LLMs for Suicide Screening with the Columbia-Suicide Severity Rating Scale:

Suicide prevention remains a critical public health challenge. While online platforms such as Reddit's r/SuicideWatch have historically provided spaces for individuals to express suicidal thoughts and seek community support, the advent of large language models (LLMs) introduces a new paradigm-where individuals may begin disclosing ideation to AI systems instead of humans. This study evaluates the capability of LLMs to perform automated suicide risk assessment using the Columbia-Suicide Severity Rating Scale (C-SSRS). We assess the zero-shot performance of six models-including Claude, GPT, Mistral, and LLaMA-in classifying posts across a 7-point severity scale (Levels 0-6). Results indicate that Claude and GPT closely align with human annotations, while Mistral achieves the lowest ordinal prediction error. Most models exhibit ordinal sensitivity, with misclassifications typically occurring between adjacent severity levels. We further analyze confusion patterns, misclassification sources, and ethical considerations, underscoring the importance of human oversight, transparency, and cautious deployment. Full code and supplementary materials are available at https://github.com/av9ash/llm_cssrs_code.


## License and Citation
This project is released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.  
Any use or reuse of this work please cite the following:

```bibtex
@article{patil2025evaluating,
  title={Evaluating Reasoning LLMs for Suicide Screening with the Columbia-Suicide Severity Rating Scale},
  author={Patil, Avinash and Tao, Siru and Gedhu, Amardeep},
  journal={arXiv preprint arXiv:2505.13480},
  year={2025}
}
```

For more details on the license, visit [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).



