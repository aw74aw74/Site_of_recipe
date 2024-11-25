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
    
    Правила:
    1. Если строка заканчивается ":", то это название этапа
    2. Если в начале строки этапа стоит цифра, она идет на номер
    3. Все следующие строки - подэтапы (до пустой строки)
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
            
        # Строка заканчивается на ":" - это новый этап
        if line.endswith(':'):
            # Завершаем предыдущий этап, если он есть
            if current_step:
                current_step['substeps'] = current_substeps
                steps.append(current_step)
                current_substeps = []
            
            # Проверяем, начинается ли строка с цифры
            step_match = re.match(r'^(\d+)\.\s*(.+):$', line)
            if step_match:
                number = step_match.group(1)
                title = step_match.group(2)
            else:
                number = None
                title = line[:-1]  # Убираем двоеточие
            
            current_step = {
                'number': number,
                'title': title,
                'substeps': []
            }
        
        # Если есть текущий этап и это не пустая строка - это подэтап
        elif current_step and line:
            current_substeps.append(line)
    
    # Добавляем последний этап, если он есть
    if current_step:
        current_step['substeps'] = current_substeps
        steps.append(current_step)
    
    return steps
