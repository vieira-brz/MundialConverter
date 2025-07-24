from typing import Union, Optional, Dict, Any, List, Tuple
import base64
import io
import os
from PIL import Image, ImageEnhance, ImageFilter
import mimetypes

class ImageConverter:
    """Classe para conversão entre diferentes formatos de imagem"""
    
    # Formatos suportados
    SUPPORTED_FORMATS = {
        'jpeg': {'extensions': ['.jpg', '.jpeg'], 'mime': 'image/jpeg', 'name': 'JPEG'},
        'png': {'extensions': ['.png'], 'mime': 'image/png', 'name': 'PNG'},
        'webp': {'extensions': ['.webp'], 'mime': 'image/webp', 'name': 'WebP'},
        'bmp': {'extensions': ['.bmp'], 'mime': 'image/bmp', 'name': 'BMP'},
        'gif': {'extensions': ['.gif'], 'mime': 'image/gif', 'name': 'GIF'},
        'tiff': {'extensions': ['.tiff', '.tif'], 'mime': 'image/tiff', 'name': 'TIFF'},
        'ico': {'extensions': ['.ico'], 'mime': 'image/x-icon', 'name': 'ICO'},
        'pdf': {'extensions': ['.pdf'], 'mime': 'application/pdf', 'name': 'PDF'}
    }
    
    # Qualidades padrão por formato
    DEFAULT_QUALITY = {
        'jpeg': 85,
        'webp': 80,
        'pdf': 95
    }
    
    @classmethod
    def detect_format(cls, file_path: str = None, data: bytes = None) -> str:
        """Detecta o formato da imagem"""
        if file_path:
            # Detecta por extensão
            _, ext = os.path.splitext(file_path.lower())
            for format_name, info in cls.SUPPORTED_FORMATS.items():
                if ext in info['extensions']:
                    return format_name
        
        if data:
            # Detecta por assinatura de bytes
            if data.startswith(b'\xff\xd8\xff'):
                return 'jpeg'
            elif data.startswith(b'\x89PNG\r\n\x1a\n'):
                return 'png'
            elif data.startswith(b'RIFF') and b'WEBP' in data[:12]:
                return 'webp'
            elif data.startswith(b'BM'):
                return 'bmp'
            elif data.startswith(b'GIF8'):
                return 'gif'
            elif data.startswith(b'II*\x00') or data.startswith(b'MM\x00*'):
                return 'tiff'
            elif data.startswith(b'\x00\x00\x01\x00'):
                return 'ico'
            elif data.startswith(b'%PDF'):
                return 'pdf'
        
        return 'unknown'
    
    @classmethod
    def load_image(cls, source: Union[str, bytes, Image.Image]) -> Image.Image:
        """Carrega imagem de diferentes fontes"""
        if isinstance(source, Image.Image):
            return source
        elif isinstance(source, str):
            # Arquivo local
            if os.path.exists(source):
                return Image.open(source)
            # Base64 string
            elif source.startswith('data:image'):
                header, data = source.split(',', 1)
                image_data = base64.b64decode(data)
                return Image.open(io.BytesIO(image_data))
            # Base64 puro
            else:
                try:
                    image_data = base64.b64decode(source)
                    return Image.open(io.BytesIO(image_data))
                except:
                    raise ValueError(f"Não foi possível carregar imagem: {source}")
        elif isinstance(source, bytes):
            return Image.open(io.BytesIO(source))
        else:
            raise ValueError(f"Tipo de fonte não suportado: {type(source)}")
    
    @classmethod
    def save_image(cls, image: Image.Image, format_name: str, quality: int = None, **kwargs) -> bytes:
        """Salva imagem em formato específico"""
        format_name = format_name.lower()
        
        if format_name not in cls.SUPPORTED_FORMATS:
            raise ValueError(f"Formato não suportado: {format_name}")
        
        # Configurações de qualidade
        if quality is None:
            quality = cls.DEFAULT_QUALITY.get(format_name, 85)
        
        # Buffer para salvar
        buffer = io.BytesIO()
        
        # Configurações específicas por formato
        save_kwargs = {}
        
        if format_name == 'jpeg':
            # JPEG não suporta transparência
            if image.mode in ('RGBA', 'LA', 'P'):
                # Cria fundo branco
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            save_kwargs.update({'quality': quality, 'optimize': True})
            
        elif format_name == 'png':
            save_kwargs.update({'optimize': True})
            
        elif format_name == 'webp':
            save_kwargs.update({'quality': quality, 'optimize': True})
            
        elif format_name == 'gif':
            # GIF requer modo P (palette)
            if image.mode != 'P':
                image = image.convert('P', palette=Image.ADAPTIVE)
            save_kwargs.update({'optimize': True})
            
        elif format_name == 'ico':
            # ICO suporta múltiplos tamanhos
            sizes = kwargs.get('sizes', [(32, 32)])
            save_kwargs.update({'sizes': sizes})
        
        # Salva a imagem
        image.save(buffer, format=format_name.upper(), **save_kwargs)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    @classmethod
    def resize_image(cls, image: Image.Image, size: Tuple[int, int], method: str = 'lanczos') -> Image.Image:
        """Redimensiona imagem"""
        resize_methods = {
            'nearest': Image.NEAREST,
            'lanczos': Image.LANCZOS,
            'bilinear': Image.BILINEAR,
            'bicubic': Image.BICUBIC,
            'box': Image.BOX,
            'hamming': Image.HAMMING
        }
        
        method_enum = resize_methods.get(method.lower(), Image.LANCZOS)
        return image.resize(size, method_enum)
    
    @classmethod
    def get_image_info(cls, image: Image.Image) -> Dict[str, Any]:
        """Obtém informações da imagem"""
        return {
            'format': image.format,
            'mode': image.mode,
            'size': image.size,
            'width': image.width,
            'height': image.height,
            'has_transparency': image.mode in ('RGBA', 'LA', 'P') and 'transparency' in image.info,
            'info': dict(image.info) if image.info else {}
        }
    
    @classmethod
    def to_base64(cls, image_data: bytes, format_name: str) -> str:
        """Converte dados da imagem para Base64"""
        mime_type = cls.SUPPORTED_FORMATS[format_name]['mime']
        b64_data = base64.b64encode(image_data).decode('utf-8')
        return f"data:{mime_type};base64,{b64_data}"
    
    @classmethod
    def convert(cls, 
                source: Union[str, bytes, Image.Image], 
                to_format: str, 
                quality: int = None,
                resize: Tuple[int, int] = None,
                resize_method: str = 'lanczos',
                **kwargs) -> Dict[str, Any]:
        """
        Converte imagem entre diferentes formatos
        
        Args:
            source: Fonte da imagem (caminho, bytes, base64 ou objeto Image)
            to_format: Formato de destino
            quality: Qualidade da compressão (1-100)
            resize: Novo tamanho (width, height)
            resize_method: Método de redimensionamento
            **kwargs: Argumentos adicionais para salvamento
        
        Returns:
            Dict com resultado da conversão
        """
        try:
            # Carrega a imagem
            image = cls.load_image(source)
            original_info = cls.get_image_info(image)
            
            # Detecta formato original
            original_format = cls.detect_format(
                file_path=source if isinstance(source, str) and os.path.exists(source) else None
            )
            if original_format == 'unknown' and image.format:
                original_format = image.format.lower()
            
            # Redimensiona se necessário
            if resize:
                image = cls.resize_image(image, resize, resize_method)
            
            # Converte para formato de destino
            to_format = to_format.lower()
            converted_data = cls.save_image(image, to_format, quality, **kwargs)
            
            # Informações da imagem convertida
            converted_image = Image.open(io.BytesIO(converted_data))
            converted_info = cls.get_image_info(converted_image)
            
            # Calcula redução de tamanho
            original_size = len(converted_data) if isinstance(source, bytes) else os.path.getsize(source) if isinstance(source, str) and os.path.exists(source) else 0
            size_reduction = ((original_size - len(converted_data)) / original_size * 100) if original_size > 0 else 0
            
            return {
                'original_format': original_format,
                'target_format': to_format,
                'original_info': original_info,
                'converted_info': converted_info,
                'converted_data': converted_data,
                'base64': cls.to_base64(converted_data, to_format),
                'size_info': {
                    'original_bytes': original_size,
                    'converted_bytes': len(converted_data),
                    'size_reduction_percent': round(size_reduction, 2)
                },
                'conversion_settings': {
                    'quality': quality or cls.DEFAULT_QUALITY.get(to_format, 85),
                    'resize': resize,
                    'resize_method': resize_method
                }
            }
            
        except Exception as e:
            raise ValueError(f"Erro na conversão de imagem: {str(e)}")
    
    @classmethod
    def batch_convert(cls, 
                     sources: List[Union[str, bytes]], 
                     to_format: str, 
                     output_dir: str = None,
                     **kwargs) -> List[Dict[str, Any]]:
        """
        Converte múltiplas imagens em lote
        
        Args:
            sources: Lista de fontes de imagem
            to_format: Formato de destino
            output_dir: Diretório de saída (opcional)
            **kwargs: Argumentos para conversão
        
        Returns:
            Lista com resultados das conversões
        """
        results = []
        
        for i, source in enumerate(sources):
            try:
                result = cls.convert(source, to_format, **kwargs)
                
                # Salva arquivo se diretório especificado
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                    filename = f"converted_{i}.{to_format}"
                    output_path = os.path.join(output_dir, filename)
                    
                    with open(output_path, 'wb') as f:
                        f.write(result['converted_data'])
                    
                    result['output_path'] = output_path
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    'error': str(e),
                    'source': str(source)
                })
        
        return results
    
    @classmethod
    def optimize_image(cls, 
                      source: Union[str, bytes, Image.Image],
                      target_size_kb: int = None,
                      max_dimension: int = None) -> Dict[str, Any]:
        """
        Otimiza imagem para reduzir tamanho
        
        Args:
            source: Fonte da imagem
            target_size_kb: Tamanho alvo em KB
            max_dimension: Dimensão máxima (largura ou altura)
        
        Returns:
            Imagem otimizada
        """
        image = cls.load_image(source)
        original_info = cls.get_image_info(image)
        
        # Redimensiona se necessário
        if max_dimension:
            width, height = image.size
            if width > max_dimension or height > max_dimension:
                ratio = min(max_dimension / width, max_dimension / height)
                new_size = (int(width * ratio), int(height * ratio))
                image = cls.resize_image(image, new_size)
        
        # Otimiza qualidade se tamanho alvo especificado
        quality = 85
        if target_size_kb:
            target_bytes = target_size_kb * 1024
            
            # Tenta diferentes qualidades
            for q in range(85, 10, -5):
                test_data = cls.save_image(image, 'jpeg', q)
                if len(test_data) <= target_bytes:
                    quality = q
                    break
        
        # Converte para JPEG otimizado
        optimized_data = cls.save_image(image, 'jpeg', quality)
        optimized_image = Image.open(io.BytesIO(optimized_data))
        optimized_info = cls.get_image_info(optimized_image)
        
        return {
            'original_info': original_info,
            'optimized_info': optimized_info,
            'optimized_data': optimized_data,
            'base64': cls.to_base64(optimized_data, 'jpeg'),
            'optimization_settings': {
                'quality': quality,
                'max_dimension': max_dimension,
                'target_size_kb': target_size_kb
            }
        }
    
    @classmethod
    def get_supported_formats(cls) -> List[str]:
        """Retorna lista de formatos suportados"""
        return list(cls.SUPPORTED_FORMATS.keys())
    
    @classmethod
    def get_format_info(cls, format_name: str) -> Dict[str, Any]:
        """Retorna informações sobre um formato específico"""
        if format_name not in cls.SUPPORTED_FORMATS:
            raise ValueError(f"Formato não suportado: {format_name}")
        
        return cls.SUPPORTED_FORMATS[format_name].copy()

# Funções de conveniência
def convert_image(source: Union[str, bytes], to_format: str, **kwargs) -> Dict[str, Any]:
    """
    Função de conveniência para conversão rápida de imagens
    
    Args:
        source: Fonte da imagem
        to_format: Formato de destino
        **kwargs: Argumentos adicionais
    
    Returns:
        Resultado da conversão
    
    Example:
        >>> convert_image('photo.jpg', 'png')
        {'converted_data': b'...', 'base64': 'data:image/png;base64,...', ...}
    """
    return ImageConverter.convert(source, to_format, **kwargs)

def optimize_image(source: Union[str, bytes], target_size_kb: int = None, max_dimension: int = None) -> Dict[str, Any]:
    """
    Otimiza imagem para reduzir tamanho
    
    Args:
        source: Fonte da imagem
        target_size_kb: Tamanho alvo em KB
        max_dimension: Dimensão máxima
    
    Returns:
        Imagem otimizada
    """
    return ImageConverter.optimize_image(source, target_size_kb, max_dimension)

def get_image_info(source: Union[str, bytes]) -> Dict[str, Any]:
    """
    Obtém informações sobre uma imagem
    
    Args:
        source: Fonte da imagem
    
    Returns:
        Informações da imagem
    """
    image = ImageConverter.load_image(source)
    return ImageConverter.get_image_info(image)

# Exemplo de uso
if __name__ == "__main__":
    print("🖼️ Testando ImageConverter...")
    print("=" * 50)
    
    # Nota: Para testar, você precisaria de arquivos de imagem reais
    # Este é um exemplo de como usar o conversor
    
    try:
        # Exemplo com imagem fictícia (você precisaria de uma imagem real)
        print("📋 Formatos suportados:")
        formats = ImageConverter.get_supported_formats()
        for fmt in formats:
            info = ImageConverter.get_format_info(fmt)
            print(f"   {info['name']}: {', '.join(info['extensions'])}")
        
        print("\n💡 Exemplo de uso:")
        print("   # Converter JPEG para PNG")
        print("   result = convert_image('photo.jpg', 'png')")
        print("   ")
        print("   # Otimizar imagem")
        print("   optimized = optimize_image('large_photo.jpg', target_size_kb=500)")
        print("   ")
        print("   # Conversão em lote")
        print("   results = ImageConverter.batch_convert(['img1.jpg', 'img2.png'], 'webp')")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n✅ Testes conceituais concluídos!")
    print("💡 Para testes reais, forneça arquivos de imagem válidos.")
