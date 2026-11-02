# UltraIR Analyzer

Настольное приложение для анализа инфракрасных (ИК) спектров в формате JCAMP-DX (`.jdx`). Использует предобученную модель **UltraIR** для предсказания 17 функциональных групп. Результаты модели — вспомогательные оценки, а не окончательная идентификация вещества или калиброванные вероятности.

## Возможности

- Загрузка `.jdx`, предобработка и нормализация спектра (400–4000 см⁻¹, 3600 точек).
- Предсказание функциональных групп на CPU с помощью UltraIR.
- Отображение графика и оценок модели в интерфейсе PySide6.
- Сохранение `prediction.json` и `spectrum.png` в `results/candidateN/`.
- Необязательная научная интерпретация на русском языке: локальная справочная база (RAG) + Groq API. Для неё нужен API-ключ и доступ к сети; без ключа основной анализ работает локально.

## Технологии

Python 3.11; **PySide6** — интерфейс; **PyTorch CPU** и **UltraIR** — инференс; **NumPy** — обработка спектров; **Matplotlib** — графики; **Groq** — дополнительная LLM-интерпретация.

## Установка (Windows, Git Bash + Miniconda)

1. Создайте окружение и активируйте его:

   ```bash
   # Если Git Bash не видит conda, а Miniconda установлена в домашнем каталоге:
   source "$HOME/miniconda3/etc/profile.d/conda.sh"
   conda create -n ultrair python=3.11 -y
   conda activate ultrair
   ```

2. Установите CPU-версию PyTorch 2.6.0:

   ```bash
   python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
   ```

3. Разместите исходные репозитории рядом и установите оригинальный UltraIR:

   ```text
   model/
   ├── UltraIR/
   └── ultrair-research/
   ```

   Из каталога `model`:

   ```bash
   git clone https://github.com/AIMS-Lab-HKUSTGZ/UltraIR.git
   cd UltraIR
   python -m pip install -e .
   ```

4. Загрузите предобученные веса из [UltraIR на Hugging Face](https://huggingface.co/yusentan/UltraIR):

   ```bash
   python -m pip install huggingface_hub
   hf download yusentan/UltraIR checkpoints/functional_group_prediction/ultrair_nist.pt --local-dir .
   ```

   Проверьте наличие `UltraIR/configs/functional_group_prediction/nist.yaml` и `UltraIR/checkpoints/functional_group_prediction/ultrair_nist.pt`.

5. Установите зависимости приложения:

   ```bash
   cd ../ultrair-research
   python -m pip install -r requirements.txt
   ```

## Запуск

Из каталога `ultrair-research` в активированном окружении:

```bash
python main.py
```

## Использование

1. Нажмите **«Выбрать JDX-файл»** и укажите спектр `.jdx`.
2. Нажмите **«Анализировать»**.
3. Посмотрите график спектра и предсказанные функциональные группы. Файлы сохраняются в `results/candidateN/`.
4. Для дополнительной интерпретации введите **Groq API Key** перед анализом. Интерпретация использует предсказания и справочные данные, но не проверяет автоматически наличие конкретных пиков в исходном спектре.

## UltraIR и авторство

Приложение использует оригинальный проект **[UltraIR](https://github.com/AIMS-Lab-HKUSTGZ/UltraIR)** исследовательской группы AIMS Lab (HKUST Guangzhou) и [опубликованные предобученные веса](https://huggingface.co/yusentan/UltraIR). 
