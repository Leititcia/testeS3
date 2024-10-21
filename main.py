import boto3
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/imagens', methods=['GET'])
def get_imagens():
    # Nome do bucket e perfil que você quer usar
    bucket_name = 'myaawsimagee'
    profile_name = 'my-dev-profile'

    # Configurar boto3 para usar o perfil específico
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')

    # Fazer a solicitação para listar os objetos no bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Verificar se há objetos no bucket e gerar URLs pré-assinadas
    imagens = []
    if 'Contents' in response:
        for obj in response['Contents']:
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': obj['Key']},
                ExpiresIn=3600  # A URL expira em 1 hora
            )
            imagens.append(url)

    return jsonify(imagens)

if __name__ == '__main__':
    app.run(debug=True)
