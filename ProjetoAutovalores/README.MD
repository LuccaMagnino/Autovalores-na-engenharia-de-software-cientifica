## Pré-requisitos

Para executar este projeto, você precisará ter o Python instalado em seu computador. Para realizar o download da versão mais recente, segue o [Site Oficial](https://www.python.org/downloads/).

Além disso, o algoritmo utiliza bibliotecas externas para a manipulação de matrizes e a geração dos gráficos de escalabilidade (numpy e matplotlib). Para instalar as dependências necessárias, após clonar todo o repositório em seu computador, abra o seu terminal e execute o seguinte comando:  

```
pip install -r requirements.txt

```
 
## Como Executar

Faça o clone deste repositório  em sua máquina local ou baixe os arquivos fonte.  

Abra o terminal e navegue até a pasta onde os arquivos do projeto foram salvos.

Execute o script principal digitando o comando abaixo:

```
python main.py

```

### EXPLICANDO CADA FUNÇÃO:

As funções foram divididas em arquivos, facilitando a leitura e entendimento do código. Os passos em ordem são os seguintes:

## Hessenberg

O arquivo hessenberg.py contém uma função para reduzir uma matriz A à forma de Hessenberg usando transformações de Householder, retornada a matriz de Hessenberg H. A função deve seguir os seguintes passos:
1. Criar uma cópia da matriz A para trabalhar, garantindo que os valores sejam do tipo float.
2. Iterar sobre as colunas da matriz, desconsiderando as últimas duas colunas e a primeira linha.
3. Para cada coluna k, extrair o vetor x a partir da submatriz abaixo da diagonal.
4. Calcular o comprimento do vetor x e criar o vetor de Householder v, ajustando o primeiro elemento para evitar cancelamento numérico.
5. Normalizar o vetor de Householder v.
6. Aplicar a transformação de Householder à direita e à esquerda para atualizar a matriz H.
7. Após o loop, limpar os erros de precisão do tipo float, definindo os elementos abaixo da subdiagonal como zero.
A função deve retornar a matriz de Hessenberg H resultante.

## Iteração QR

fazendo ainda
