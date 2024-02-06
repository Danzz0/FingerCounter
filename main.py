import cv2
import mediapipe as mediaP

# comandos de importação de biblioteca
        # pip install opencv-python
        # pip install mediapipe
        
video = cv2.VideoCapture(0) # variável que armazena frames da primeira câmera que estiver conectada ao pc 


hand = mediaP.solutions.hands # variável que contem o pacote de processamento de mão em video do mediaP
maos = hand.Hands(max_num_hands = 2) # Hands classe responsável por processar as imagens e detectar mãos nelas. Estou permitindo apenas 2 mãos na tela
desenhoNaTela = mediaP.solutions.drawing_utils




while True:
    sucessoNaLeitura, imagem = video.read() # read() processa 1 frame da img e retorna a imagem e um indicador de sucesso (ou não) do seu processamento

    #convertem as cores da imagem para o formato aceito pelo mediaPipe
    imagemRgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    maoProcessada = maos.process(imagemRgb)

    handPoints = maoProcessada.multi_hand_landmarks
    altura, largura, _ = imagem.shape
    pontos = []
    if handPoints:
        for points in handPoints:

            desenhoNaTela.draw_landmarks(imagem, points, hand.HAND_CONNECTIONS)

            for identificador, cord in enumerate(points.landmark):
                eixoX = int(cord.x * largura)
                eixoY = int(cord.y * altura)

                # cv2.putText(imagem, str(identificador), (eixoX, eixoY+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                pontos.append((eixoX, eixoY))
                
        dedos = [ 8, 12, 16, 20]
        contador = 0

        if points:
            if pontos[4][0] < pontos[2][0]:
                contador += 1
            for i in dedos:
                if pontos[i][1] < pontos[i-2][1]: # se o ponto superior do dedo estiver acima do ponto da junta do dedo (dedo levantado) o contador aumenta
                    contador += 1
                    #quanto menor for o número do eixo y, a altura aumenta

        # contador exibido na tela    
        cv2.putText(imagem, str(contador), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,0,0), 5)

    cv2.imshow("Imagem", imagem)
    encerrar = cv2.waitKey(1)
    
    if(encerrar == ord('z')):
        break

video.release()
cv2.destroyAllWindows()
    
