# Анализ выполнения первого занятия

В целом первый пример не сложный, так как относительно учебного примера изменилась только команда `push`
и теперь она может быть не выполнена корректно (т.е. появилось новое предусловие и нужно добавить проверку статуса выполнения)
однако:

1. Упустил постусловие для конструктора, его не было в примере, а сам не догадался, впредь буду обращать внимание
2. В шаблоне константы для статуса PUSH всего 2, это ошибка и успешное выполнение, нет константы, отвечающей за проверку до выполнения.
У себе реализовал также возможность, что `push` еще не вызывался, мне кажется что это возможно, если мы запросим проверку статуса
сразу после создания пустого стека.
