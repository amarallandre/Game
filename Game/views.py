from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
import logging
from .models import Char
from django.http import HttpResponse, JsonResponse
import xml.etree.ElementTree as ET


logger = logging.getLogger(__name__)

def Char_Creator(request):
    if request.method == 'POST':
        select_class = request.POST.get('class')
        char_name = request.POST.get('name')


        xml_path = f'Game/xml_data/{select_class}.xml'
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()


            new_char = Char.objects.create(
                name=char_name,
                job=root.find('job').text,
                life=int(root.find('life').text),
                attack=int(root.find('attack').text),
                defense=int(root.find('defense').text),
            )

            return HttpResponse(f'Char {new_char.name} created with successful!')
        except FileNotFoundError:
            return HttpResponse('Class no found!')
        except Exception as e:
            return HttpResponse(f'Error to create the char: {str(e)}')

    return render(request, 'Game/Main.html')


def get_all_chars(request):
    all_chars = Char.objects.all()
    char_data = [{'name': char.name, 'job': char.job} for char in all_chars]
    return JsonResponse(char_data, safe=False)

def delete_char(request):
    if request.method == 'POST':
        char_name = request.POST.get('name')

        chars_to_delete = Char.objects.filter(name=char_name)
        if chars_to_delete.exists():
            chars_to_delete.first().delete()
            return JsonResponse({'message': 'Char deleted successfully.'})
        else:
            return JsonResponse({'message': 'Char not found.'}, status=404)
    else:
        return JsonResponse({'message': 'Method not allowed.'}, status=405)

def select_char(request):
    if request.method == 'POST':
        char_name = request.POST.get('name')

        if char_name is not None:
            chars_to_select = Char.objects.filter(name=char_name)
            if chars_to_select.exists():
                selected_char = chars_to_select.first()
                # Retorne todas as informações relevantes do personagem no JSON
                char_data = {
                    'id': selected_char.id,
                    'name': selected_char.name,
                    'job': selected_char.job,
                    'life': selected_char.life,
                    'attack': selected_char.attack,
                    'defense': selected_char.defense,
                    # Adicione outros campos conforme necessário
                }
                return JsonResponse(char_data)
            else:
                return JsonResponse({'message': f'No character found with the name: {char_name}'})
        else:
            return JsonResponse({'message': 'Invalid request. Character name not provided.'}, status=400)

    return JsonResponse({'message': 'Invalid request. Method not allowed.'}, status=405)
def game_page(request):
    # Obtenha o nome do personagem do parâmetro na URL
    char_name = request.GET.get('name')

    # Faça o que for necessário com o nome do personagem
    # (por exemplo, recuperar dados do personagem do banco de dados)
    try:
        character = Char.objects.get(name=char_name)
        char_data = {
            'char_name': character.name,
            'char_job': character.job,
            'char_life': character.life,
            'char_attack': character.attack,
            'char_defense': character.defense,
            # Adicione outros campos conforme necessário
        }
    except Char.DoesNotExist:
        # Trate o caso em que o personagem não é encontrado
        char_data = {
            'char_name': 'Personagem não encontrado',
            'char_job': '',
            'char_life': 0,
            'char_attack': 0,
            'char_defense': 0,
            # Adicione outros campos conforme necessário
        }

    # Renderize a página HTML do jogo com os dados do personagem
    return render(request, 'Game/Game.html', char_data)