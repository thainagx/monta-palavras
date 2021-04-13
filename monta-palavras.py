# Importações para tratamento de entradas de caracteres especiais, acentos e números
import unicodedata
import re

# Banco de palavras possíveis
word_bank = ["Abacaxi", "Manada", "Mandar", "Porta", "Mesa", "Dado", "Mangas", "Já", "Coisas", "Radiografia", "Matemática", "Drogas", "Prédios", "Implementação", "Computador", "Balão", "Xícara", "Tédio", "Faixa", "Livro", "Deixar", "Superior", "Profissão", "Reunião", "Prédios", "Montanha", "Botânica", "Banheiro", "Caixas", "Xingamento", "Infestação", "Cupim", "Premiada", "Empanada", "Ratos", "Ruído", "Antecedente", "Empresa", "Emissário", "Folga", "Fratura", "Goiaba", "Gratuito", "Hídrico", "Homem", "Jantar", "Jogos", "Montagem", "Manual", "Nuvem", "Neve", "Operação", "Ontem", "Pato", "Pé", "Viagem", "Queijo", "Quarto", "Quintal", "Solto", "Rota", "Selva", "Tatuagem", "Tigre", "Uva", "Último", "Vitupério", "Voltagem", "Zangado", "Zombaria", "Dor"]
# Tabela de pontuação das letras
letter_points = [('E', 1), ('A', 1), ('I', 1), ('O', 1), ('N', 1), ('R', 1), ('T', 1), ('L', 1), ('S', 1), ('U', 1), ('D', 2), ('G', 2), ('B', 3), ('C', 3), ('M', 3), ('P', 3), ('F', 5), ('H', 5), ('V', 5), ('J', 8), ('X', 8), ('Q', 13), ('Z', 13)] 

# Função responsável pelo tratamento de entradas com caracteres especiais, números e acentos
def incoming_treatment(input_letters):
    nfkd = unicodedata.normalize('NFKD', input_letters)
    new_input_letters = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return re.sub('[^a-zA-Z \\\]', '', new_input_letters).upper()

# Função responsável por realizar a contagem de pontos
def count_points(word, bonus_position):
    count = 0
    for letter, index in zip(word, range(len(word))):
        for line in range(len(letter_points)):
            if letter in letter_points[line]:
                if bonus_position >= 0 and index == bonus_position:
                    count = count + (2*letter_points[line][1])
                else:
                    count = count + letter_points[line][1]
    return count

# Função responsável por analizar as palavras do banco e validar 
# a construção de acordo com as letras de entrada
def can_construct(input_letters, word):
    if word == "":
        return True, input_letters
    for letter in input_letters:
        if word.find(letter) == 0:
            new_word = word[1:]
            index = input_letters.index(letter)
            if index > -1:
                new_input = input_letters.copy() 
                new_input.pop(index)
            else: 
                break
            is_possible, word_left = can_construct(new_input, new_word) 
            if(is_possible == True):
                return True, word_left
    return False, input_letters

# Descrição da lógica do programa:
# Foi feito um laço infinito para a chamada da função principal, para produzir uma repetição do programa.
# No começo do programa inicializamos as variáveis que serão utilizadas no decorrer do algoritmo.
# Após capturarmos as informações do usuário, fazemos o tratamento da entrada e transformamos a string em array.
# Descrição da função incoming_treatment():
# Com a entrada da string com as letras utilizadas, normalizamos o caracter em comparação com seu 
# correspondente em Latim, depois percorremos cada letra tirando os acentos existentes. E por fim retornamos
# a expressão somente com letras todas em maiúsculo.
# Após o tratamento da entrada e a captura da posição bônus, percorremos as palavras no banco. Para cada 
# palavra fazemos a chamada da função can_construct().
# Descrição da função can_construct():
# A função é recursiva e recebe como entrada uma lista de letras e uma string.
# Se a string for vazia (caso de parada), a função retorna True confirmando o fim do processo e o resto das letras que sobraram.
# Caso a string não seja vazia, é feito um laço percorrendo cada item na lista de letras comparando com a primeira letra da string.
# Se as letras forem correspondentes, é criada uma nova palavra (new_word) retirando a primeira letra.
# Com a variável index pesquisamos na lista de letras qual a posição da letra analisada, criamos uma nova variável (new_imput)
# para fazer uma cópia das letras de entrada e com a função pop() retiramos a letra do conjunto.
# E fazemos a chamada recursiva, caso a palavra seja possível de ser construída, a função retorna true e as letras que sobraram
# Caso a palavra não seja possível, a função retorna False e a lista de letras de entrada.
# Após a verificação da construção da palavra analisada, se caso for possível, fazemos a chamada de contagem de pontos.
# Descrição da função count_points():
# Inicializamos a variável count que guardará a pontuação final da palavra, e fazemos um laço percorrendo cada letra na palavra do banco
# analisada e juntamente com seu index, que é o caso do for de duas variáveis.
# Como a tabela de pontos é uma lista de tuplas, fazemos a verificação por linha se a letra em questão está naquela linha,
# caso a letra esteja naquela tupla, fazemos uma comparação do index para ver se é o mesmo da posição bônus, lembrando que na condição
# do if adicionamos o caso da bonus_position for menor que zero, nesse caso, a pessoa quer que desconsidere a posição bônus naquela jogada.
# Após a contagem de pontos da palavra analisada, fazemos uma comparação com a maior pontuação obtida até o momento, caso a palavra atual tenha
# uma maior pontuação, atualizamos as informações de best_word, leftover_letters e count. Se a pontuação for igual a maior anterior, fazemos
# uma análise do tamanho das palavras, retornando a menor, e se, por acaso a palavra tiver o mesmo tamanho, retornamos a palavra que vem primeiro
# em ordem alfabética. 
# E por fim, retornamos as informações finais da jogada.

def main():
    count = 0 # Variável responsável por armazenar a contagem final da jogada
    best_word = "" # Variável responsável por armazenar a melhor palavra da jogada
    leftover_letters = "" # Variável responsável por armazenar as letras que sobram da jogada
    input_letters = input("Digite as letras disponíveis nesta jogada: ")
    # Chamada para o tratamento da entrada de letras
    input_letters = list(incoming_treatment(input_letters)) 
    bonus_position = int(input("Digite a posição bônus: "))
    # Laço para percorrer o banco de palavras
    for word in word_bank:  
        # Chamada para a verificação de palavras possíveis
        is_possible, letters_left = can_construct(input_letters, incoming_treatment(word))
        # Condição para a palavra que é possível ser construída pelas letras de entrada
        if is_possible == True:
            # Chamada da contagem de pontos
            word_points = count_points(incoming_treatment(word), bonus_position-1)
            # Comparação da maior pontuação até o momento
            if word_points > count:
                # Atualização das informações finais, caso a palavra em questão
                # tenha uma pontuação maior do que a palavra de maior pontuação anterior
                count = word_points
                best_word = word
                leftover_letters = letters_left
            # Condição de empate entre as pontuações de duas palavras
            elif word_points == count:
                # Comparação dos tamanhos das palavras de maior pontuação até o momento
                if len(best_word) > len(word):
                    # Atualização das informações caso a palavra atual tenha um número menor de letras
                    best_word = word
                    leftover_letters = letters_left
                # Condição para avaliar as palavras em comparação que possuem o mesmo tamanho 
                elif len(best_word) == len(word):
                    # Condição escolher a palavra que vem primeiro tomando em conta
                    # a ordem alfabética
                    if best_word > word:
                        best_word = word
    # Retorno para o caso de não encontrar nenhuma palavra
    if best_word == "":
        print("\nNenhuma palavra encontrada\nSobraram: 0")
    # Retorno para o caso de ser possível construir uma palavra do banco
    else:
        print("\n", best_word.upper(), ", palavra de", count, "pontos\nSobraram:", leftover_letters)

# Chamada da função principal        
if __name__ == "__main__":
    while 1:
        main()