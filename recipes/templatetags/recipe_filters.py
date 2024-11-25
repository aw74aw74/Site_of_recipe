from django import template
import re

register = template.Library()

@register.filter
def split(value, arg):
    """
    Splits a string by the given argument.
    Usage: {{ value|split:"delimiter" }}
    """
    return value.split(arg)

@register.filter
def strip(value):
    """
    Removes leading and trailing whitespace.
    Usage: {{ value|strip }}
    """
    return value.strip() if value else value

@register.filter
def get_substeps(steps, index):
    """
    Returns a list of substeps for the given step index.
    Substeps are lines starting with '-' or '•' that follow the main step.
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
    Parses ingredients text into blocks.
    Each block starts with a line ending with ':' and ends with a double newline.
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
    Парсит текст шагов приготовления в структурированный формат.
    
    Поддерживает различные форматы:
    1. Этапы с двоеточием в конце и подэтапами
    2. Нумерованные шаги без двоеточия
    3. Простой список шагов
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
