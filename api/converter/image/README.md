# 🖼️ Image Converter

Conversor robusto entre diferentes formatos de imagem com otimização, redimensionamento e processamento avançado usando PIL/Pillow.

## ✨ Características

- **Múltiplos Formatos**: Suporte para 8 formatos de imagem populares
- **Detecção Automática**: Identifica formato por extensão ou assinatura de bytes
- **Otimização Inteligente**: Compressão e redimensionamento automático
- **Base64 Support**: Conversão para/de Base64 com data URLs
- **Processamento em Lote**: Conversão de múltiplas imagens simultaneamente
- **Preservação de Qualidade**: Configurações avançadas de qualidade e compressão

## 🎯 Formatos Suportados

| Formato | Extensões | MIME Type | Características |
|---------|-----------|-----------|-----------------|
| **JPEG** | `.jpg`, `.jpeg` | `image/jpeg` | Compressão com perda, ideal para fotos |
| **PNG** | `.png` | `image/png` | Sem perda, suporte a transparência |
| **WebP** | `.webp` | `image/webp` | Moderno, alta compressão |
| **BMP** | `.bmp` | `image/bmp` | Sem compressão, compatibilidade |
| **GIF** | `.gif` | `image/gif` | Animações, paleta limitada |
| **TIFF** | `.tiff`, `.tif` | `image/tiff` | Alta qualidade, uso profissional |
| **ICO** | `.ico` | `image/x-icon` | Ícones, múltiplos tamanhos |
| **PDF** | `.pdf` | `application/pdf` | Documentos com imagens |

## 🚀 Como Usar

### Importação
```python
from api.converter.image.image import ImageConverter, convert_image, optimize_image
```

### Conversão Básica
```python
# Converter JPEG para PNG
result = convert_image('photo.jpg', 'png')
print(f"Conversão concluída: {len(result['converted_data'])} bytes")

# Salvar resultado
with open('photo.png', 'wb') as f:
    f.write(result['converted_data'])
```

### Conversão com Redimensionamento
```python
# Redimensionar e converter
result = ImageConverter.convert(
    'large_photo.jpg', 
    'webp', 
    resize=(800, 600),
    quality=80
)

# Base64 para uso em web
base64_image = result['base64']
print(f"Data URL: {base64_image[:50]}...")
```

### Otimização de Imagens
```python
# Otimizar para tamanho específico
optimized = optimize_image(
    'large_photo.jpg',
    target_size_kb=500,  # Máximo 500KB
    max_dimension=1200   # Máximo 1200px
)

print(f"Tamanho original: {optimized['original_info']['size']}")
print(f"Tamanho otimizado: {optimized['optimized_info']['size']}")
```

## 📋 Exemplos Práticos

### Web Development
```python
# Converter para WebP (melhor para web)
result = convert_image('banner.jpg', 'webp', quality=85)

# Criar thumbnails
thumbnail = ImageConverter.convert(
    'product.jpg',
    'jpeg',
    resize=(300, 300),
    quality=75
)

# Gerar ícones
icon_result = ImageConverter.convert(
    'logo.png',
    'ico',
    resize=(32, 32),
    sizes=[(16, 16), (32, 32), (48, 48)]
)
```

### E-commerce
```python
# Otimizar imagens de produtos
products = ['prod1.jpg', 'prod2.png', 'prod3.jpeg']

optimized_products = ImageConverter.batch_convert(
    products,
    'webp',
    output_dir='optimized/',
    quality=80,
    resize=(800, 800)
)

for result in optimized_products:
    if 'error' not in result:
        reduction = result['size_info']['size_reduction_percent']
        print(f"Redução de tamanho: {reduction}%")
```

### Processamento de Documentos
```python
# Converter scans para PDF
scans = ['scan1.jpg', 'scan2.jpg', 'scan3.jpg']

pdf_results = ImageConverter.batch_convert(
    scans,
    'pdf',
    quality=95,
    output_dir='pdfs/'
)
```

### Redes Sociais
```python
# Redimensionar para diferentes plataformas
social_sizes = {
    'instagram_post': (1080, 1080),
    'facebook_cover': (820, 312),
    'twitter_header': (1500, 500)
}

original_image = 'content.jpg'

for platform, size in social_sizes.items():
    result = convert_image(
        original_image,
        'jpeg',
        resize=size,
        quality=85
    )
    
    with open(f'{platform}.jpg', 'wb') as f:
        f.write(result['converted_data'])
```

## 🔧 Métodos da Classe

### `ImageConverter.convert(source, to_format, **options)`
Método principal de conversão entre formatos.

**Parâmetros:**
- `source`: Caminho, bytes, base64 ou objeto PIL Image
- `to_format`: Formato de destino
- `quality`: Qualidade de compressão (1-100)
- `resize`: Novo tamanho (width, height)
- `resize_method`: Método de redimensionamento

### `ImageConverter.batch_convert(sources, to_format, **options)`
Conversão em lote de múltiplas imagens.

### `ImageConverter.optimize_image(source, target_size_kb, max_dimension)`
Otimização automática de imagens.

### `ImageConverter.detect_format(file_path, data)`
Detecção automática de formato.

### `ImageConverter.get_image_info(image)`
Informações detalhadas da imagem.

## 📊 Estrutura de Retorno

```python
{
    'original_format': 'jpeg',
    'target_format': 'png',
    'original_info': {
        'format': 'JPEG',
        'mode': 'RGB',
        'size': (1920, 1080),
        'width': 1920,
        'height': 1080,
        'has_transparency': False
    },
    'converted_info': {
        'format': 'PNG',
        'mode': 'RGB',
        'size': (800, 450),
        'width': 800,
        'height': 450,
        'has_transparency': False
    },
    'converted_data': b'...',  # Dados binários da imagem
    'base64': 'data:image/png;base64,iVBOR...',
    'size_info': {
        'original_bytes': 245760,
        'converted_bytes': 89432,
        'size_reduction_percent': 63.6
    },
    'conversion_settings': {
        'quality': 85,
        'resize': (800, 450),
        'resize_method': 'lanczos'
    }
}
```

## 🎨 Métodos de Redimensionamento

| Método | Características | Uso Recomendado |
|--------|-----------------|-----------------|
| `lanczos` | Alta qualidade, mais lento | Fotos, imagens detalhadas |
| `bicubic` | Boa qualidade, velocidade média | Uso geral |
| `bilinear` | Qualidade média, rápido | Thumbnails |
| `nearest` | Baixa qualidade, muito rápido | Pixel art, ícones pequenos |
| `box` | Boa para redução | Downscaling |
| `hamming` | Suave, boa para redução | Imagens com texto |

```python
# Exemplo de diferentes métodos
methods = ['lanczos', 'bicubic', 'bilinear']

for method in methods:
    result = convert_image(
        'photo.jpg',
        'png',
        resize=(400, 300),
        resize_method=method
    )
    
    with open(f'resized_{method}.png', 'wb') as f:
        f.write(result['converted_data'])
```

## 🔍 Detecção Automática de Formato

O conversor detecta formatos por:

### Extensão de Arquivo
```python
format = ImageConverter.detect_format(file_path='image.jpg')  # 'jpeg'
```

### Assinatura de Bytes (Magic Numbers)
```python
with open('image.jpg', 'rb') as f:
    data = f.read(12)
    format = ImageConverter.detect_format(data=data)  # 'jpeg'
```

### Assinaturas Suportadas
- **JPEG**: `FF D8 FF`
- **PNG**: `89 50 4E 47 0D 0A 1A 0A`
- **WebP**: `RIFF...WEBP`
- **BMP**: `42 4D`
- **GIF**: `47 49 46 38`
- **TIFF**: `49 49 2A 00` ou `4D 4D 00 2A`
- **ICO**: `00 00 01 00`
- **PDF**: `25 50 44 46`

## 💾 Trabalhando com Base64

### Converter para Base64
```python
result = convert_image('photo.jpg', 'png')
base64_url = result['base64']

# Usar em HTML
html = f'<img src="{base64_url}" alt="Converted Image">'
```

### Converter de Base64
```python
# Base64 com data URL
base64_string = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
result = convert_image(base64_string, 'png')

# Base64 puro
pure_base64 = "/9j/4AAQSkZJRgABAQEA..."
result = convert_image(pure_base64, 'webp')
```

## ⚡ Otimização Avançada

### Por Tamanho de Arquivo
```python
# Otimizar para máximo 200KB
optimized = optimize_image(
    'large_image.jpg',
    target_size_kb=200
)

print(f"Qualidade aplicada: {optimized['optimization_settings']['quality']}")
```

### Por Dimensões
```python
# Limitar dimensão máxima
optimized = optimize_image(
    'huge_image.jpg',
    max_dimension=1024  # Máximo 1024px em qualquer lado
)
```

### Combinado
```python
# Otimização completa
optimized = optimize_image(
    'original.jpg',
    target_size_kb=500,
    max_dimension=1200
)
```

## 🔄 Conversão em Lote

### Básica
```python
images = ['img1.jpg', 'img2.png', 'img3.gif']

results = ImageConverter.batch_convert(
    images,
    'webp',
    quality=80
)

for i, result in enumerate(results):
    if 'error' in result:
        print(f"Erro na imagem {i}: {result['error']}")
    else:
        print(f"Imagem {i} convertida com sucesso")
```

### Com Saída em Diretório
```python
results = ImageConverter.batch_convert(
    images,
    'webp',
    output_dir='converted/',
    quality=85,
    resize=(800, 600)
)

# Arquivos salvos automaticamente em 'converted/'
```

## 🎯 Casos de Uso Específicos

### Galeria de Fotos
```python
def process_photo_gallery(input_dir, output_dir):
    import glob
    
    # Encontrar todas as imagens
    image_files = glob.glob(f"{input_dir}/*.{jpg,jpeg,png}")
    
    # Processar em lote
    results = ImageConverter.batch_convert(
        image_files,
        'webp',
        output_dir=output_dir,
        quality=85,
        resize=(1200, 800)
    )
    
    return results
```

### Avatar/Profile Pictures
```python
def create_profile_pictures(source_image):
    sizes = {
        'thumbnail': (64, 64),
        'small': (128, 128),
        'medium': (256, 256),
        'large': (512, 512)
    }
    
    avatars = {}
    
    for size_name, dimensions in sizes.items():
        result = convert_image(
            source_image,
            'png',
            resize=dimensions,
            quality=90
        )
        avatars[size_name] = result['base64']
    
    return avatars
```

### Compressão para Email
```python
def prepare_for_email(image_path, max_size_kb=500):
    # Otimizar para email
    optimized = optimize_image(
        image_path,
        target_size_kb=max_size_kb,
        max_dimension=800
    )
    
    # Converter para JPEG se necessário
    if optimized['optimized_info']['format'] != 'JPEG':
        final_result = convert_image(
            optimized['optimized_data'],
            'jpeg',
            quality=85
        )
        return final_result['converted_data']
    
    return optimized['optimized_data']
```

## ⚠️ Limitações e Considerações

### Transparência
- **JPEG**: Não suporta transparência (fundo branco adicionado automaticamente)
- **PNG/WebP**: Suporte completo à transparência
- **GIF**: Transparência binária (sim/não)

### Animações
- **GIF**: Apenas primeiro frame é processado
- **WebP**: Animações não suportadas nesta versão

### Memória
- Imagens muito grandes podem consumir muita RAM
- Use processamento em lote para múltiplas imagens pequenas

### Qualidade
- Conversões com perda (JPEG, WebP) reduzem qualidade
- Múltiplas conversões degradam progressivamente

## 🧪 Testando

Execute o arquivo diretamente para ver exemplos:

```bash
python image.py
```

## 📦 Dependências

```bash
pip install Pillow
```

## 🔄 Integração com Outros Conversores

O Image Converter pode ser usado em conjunto com outros conversores do MundialConverter:

```python
# Exemplo: Converter imagem e gerar relatório
from api.converter.text.text import TextConverter

# Processar imagem
result = convert_image('document.jpg', 'png')

# Gerar relatório de texto
report = TextConverter.generate_statistics(f"Imagem convertida: {result['original_format']} → {result['target_format']}")
```

## 🎨 Exemplos Visuais

### Antes e Depois
```python
def show_conversion_stats(source, target_format):
    result = convert_image(source, target_format, quality=80)
    
    print(f"📊 Estatísticas da Conversão:")
    print(f"   Original: {result['original_format'].upper()}")
    print(f"   Convertido: {result['target_format'].upper()}")
    print(f"   Tamanho: {result['original_info']['size']}")
    print(f"   Redução: {result['size_info']['size_reduction_percent']}%")
    
    return result
```

O Image Converter oferece uma solução completa para todas as necessidades de conversão e processamento de imagens em Python!
