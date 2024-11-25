from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from utils import utils
from produtos.models import Variacao
from .models import Pedido, ItemPedido

class Pagar(View):
    ...
        

class SalvarPedido(View):
    template_name = 'pedido/pagar.html'
    
    def get(self, *args, **kwargs):

        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você precisa fazer login.')
            return redirect('perfil:criar')
        
        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carrinho vazio.')
            return redirect('produto:lista')

        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho]
        bd_variacoes = list(Variacao.objects.select_related('produto').filter(if__in=carrinho_variacao_ids))

        for variacao in bd_variacoes:
            vid = str(variacao.id)
            
            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque = 'Estoque insufiente para alguns produtos do seu carrinho. ' \
                               'Reduzimos a quantidade desses produtos, por favor verifique no resumo da compra.'

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unt_promo
            
            if error_msg_estoque:
                messages.error(self.request, error_msg_estoque)

                self.request.session.save()
                return redirect('produto:carrinho')
            
        quantidade_total = utils.cart_total_qtd(carrinho)
        valor_total = utils.cart_total(carrinho)

        pedido = Pedido(usuario=self.request.user, total=valor_total, qtd_total=quantidade_total, status='C')
        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )

        contexto = {
            'quantidade_total': quantidade_total,
            'valor_total': valor_total
        }

        del self.request.session['carrinho']

        return redirect('pedido:lista')

class Detalhe(View):
    ...
    
class Lista():
    ...