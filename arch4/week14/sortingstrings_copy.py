o
    *�c�  �                   @   s0   d e defdd�Zdd� Zedkre�  dS dS )�inp�returnc                    s&   g d�� t tt� fdd�| ���}|S )N)�a�e�i�ur   �oc                    s   | � � � v S )N)�lower)�x�Zletters� �sortingstrings_copy.py�<lambda>   s    z#get_num_of_vowels.<locals>.<lambda>)�len�list�filter)r   Zvowel_countr   r
   r   �get_num_of_vowels   s   r   c                  C   s   g d�} t t| td�� d S )N)�codeZprogramming�descriptionZfly�free)�key)�print�sortedr   )�casesr   r   r   �sort_basedon_vowels	   s   r   �__main__N)�str�intr   r   �__name__r   r   r   r   �<module>   s
    
�