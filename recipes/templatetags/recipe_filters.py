"""
Пользовательские фильтры шаблонов для приложения рецептов.

Этот модуль содержит набор фильтров для обработки текста в шаблонах Django,
специально разработанных для форматирования рецептов, ингредиентов и шагов
приготовления.
"""

from django import template
import re

register = template.Library()

@register.filter
def split(value, arg):
    """
    Разделяет строку по указанному разделителю.
    
    Args:
        value: Исходная строка
        arg: Разделитель
    
    Returns:
        list: Список подстрок
    
    Использование в шаблоне: 
        {{ value|split:"разделитель" }}
    """
    return value.split(arg)

@register.filter
def strip(value):
    """
    Удаляет начальные и конечные пробелы из строки.
    
    Args:
        value: Исходная строка
    
    Returns:
        str: Строка без начальных и конечных пробелов
    
    Использование в шаблоне:
        {{ value|strip }}
    """
    return value.strip() if value else value

@register.filter
def get_substeps(steps, index):
    """
    Возвращает список подшагов для указанного шага.
    
    Подшаги - это строки, начинающиеся с '-' или '•', 
    которые следуют за основным шагом.
    
    Args:
        steps: Список всех шагов
        index: Индекс основного шага
    
    Returns:
        list: Список подшагов
    """
    if not steps or not isinstance(steps, list) or index >= len(steps):
        return []
    
    substeps = []
    current_index = index + 1
    
    while current_index < len(steps):
        step = steps[current_index].strip()
        if step.startswith('-') or step.startswith('•'):
            substeps.append(step)
            current_index += 1
        else:
            break
    
    return substeps

@register.filter
def parse_ingredients(value):
    """
    Разбирает текст ингредиентов на блоки.
    
    Каждый блок начинается со строки, заканчивающейся двоеточием,
    и заканчивается двойным переносом строки.
    
    Args:
        value: Текст с ингредиентами
    
    Returns:
        list: Список блоков ингредиентов
    
    Пример входных данных:
        Для теста:
        - 2 стакана муки
        - 1 яйцо
        
        Для начинки:
        - 300г творога
        - 2 ст.л. сахара
    """
    if not value:
        return []
    
    lines = value.split('\n')
    blocks = []
    current_block = None
    current_items = []
    
    for line in lines:
        line = line.strip()
        if not line:  # Empty line
            if current_block is not None and current_items:
                blocks.append({
                    'title': current_block,
                    'items': current_items
                })
                current_block = None
                current_items = []
            continue
            
        if line.endswith(':'):  # New block starts
            if current_block is not None and current_items:
                blocks.append({
                    'title': current_block,
                    'items': current_items
                })
                current_items = []
            current_block = line[:-1]  # Remove the colon
        elif line:  # Regular ingredient line
            if current_block is None:
                current_items.append(line)
            else:
                current_items.append(line)
    
    # Add the last block if exists
    if current_block is not None and current_items:
        blocks.append({
            'title': current_block,
            'items': current_items
        })
    elif current_items:  # Add remaining items without a block
        blocks.append({
            'title': None,
            'items': current_items
        })
    
    return blocks

@register.filter
def parse_steps(value):
    """
    Разбирает текст шагов приготовления в структурированный формат.
    
    Поддерживает различные форматы:
    1. Этапы с двоеточием в конце и подэтапами
    2. Нумерованные шаги без двоеточия
    3. Простой список шагов
    
    Args:
        value: Текст с шагами приготовления
    
    Returns:
        list: Список структурированных шагов
    
    Пример входных данных:
        Подготовка теста:
        - Смешать муку с солью
        - Добавить яйца
        
        1. Раскатать тесто
        2. Выложить начинку
        3. Запекать при 180°C
    """
    if not value:
        return []

    steps = []
    current_step = None
    current_substeps = []
    
    # Разбиваем на строки и убираем пробелы справа
    lines = [line.rstrip() for line in value.split('\n')]
    
    for line in lines:
        line = line.strip()
        
        # Пустая строка - завершаем текущий этап
        if not line:
            if current_step:
                current_step['substeps'] = current_substeps
                steps.append(current_step)
                current_step = None
                current_substeps = []
            continue
        
        # Проверяем различные форматы строк
        step_with_colon = re.match(r'^(?:(\d+)\.\s*)?(.+):$', line)  # Шаг с двоеточием
        step_with_number = re.match(r'^(\d+)\.\s*(.+)$', line)  # Нумерованный шаг
        
        # Если это шаг с двоеточием
        if step_with_colon:
            if current_step:
                current_step['substeps'] = current_substeps
                steps.append(current_step)
                current_substeps = []
            
            number = step_with_colon.group(1)
            title = step_with_colon.group(2)
            current_step = {
                'number': number,
                'title': title,
                'substeps': []
            }
        
        # Если это нумерованный шаг без двоеточия
        elif step_with_number:
            if current_step:
                current_step['substeps'] = current_substeps
                steps.append(current_step)
                current_substeps = []
            
            number = step_with_number.group(1)
            title = step_with_number.group(2)
            current_step = {
                'number': number,
                'title': title,
                'substeps': []
            }
            # Сразу добавляем шаг, так как он не предполагает подшагов
            steps.append(current_step)
            current_step = None
            current_substeps = []
        
        # Если строка начинается с маркера списка или это обычный текст
        elif line.startswith(('-', '•', '*')):
            if current_step:
                current_substeps.append(line)
            else:
                # Если нет текущего шага, создаем новый без номера
                current_step = {
                    'number': None,
                    'title': line,
                    'substeps': []
                }
                steps.append(current_step)
                current_step = None
        else:
            if current_step:
                current_substeps.append(line)
            else:
                # Если нет текущего шага, создаем новый без номера
                current_step = {
                    'number': None,
                    'title': line,
                    'substeps': []
                }
                steps.append(current_step)
                current_step = None
    
    # Добавляем последний этап, если он есть
    if current_step:
        current_step['substeps'] = current_substeps
        steps.append(current_step)
    
    return steps
