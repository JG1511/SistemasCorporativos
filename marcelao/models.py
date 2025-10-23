from django.db import models

# Create your models here.



from django.db import models

class Correntista(models.Model):

    CorrentistaID = models.AutoField(primary_key=True) 
    NomeCorrentista = models.CharField(max_length=50)
    Saldo = models.DecimalField(max_digits=15, decimal_places=2) 

    class Meta:
        
        managed = False # esse caba aqui é para o django não recriar as tebelas, pois elas ja existem no BD
        
        
        db_table = 'Correntistas' 

    def __str__(self):
        return self.NomeCorrentista

class Movimentacao(models.Model):
    MovimentacaoID = models.IntegerField(primary_key=True) 
    

    CorrentistaID = models.ForeignKey(Correntista, on_delete=models.DO_NOTHING, db_column='CorrentistaID', related_name='movimentacoes_feitas')
    

    CorrentistaBeneficiarioID = models.ForeignKey(
        Correntista, 
        on_delete=models.DO_NOTHING, 
        db_column='CorrentistaBeneficiarioID', 
        related_name='movimentacoes_recebidas',
        null=True, blank=True
    )

    TipoOperacao = models.CharField(max_length=1)
    ValorOperacao = models.DecimalField(max_digits=15, decimal_places=2)
    DataOperacao = models.DateTimeField()
    Descricao = models.CharField(max_length=50)

    class Meta:
       
        managed = False 
        db_table = 'Movimentacoes'
        indexes = [
            models.Index(fields=['CorrentistaID']),
        ]

class VwExtrato(models.Model):

    MovimentacaoID = models.IntegerField(primary_key=True) 

    CorrentistaID = models.IntegerField()
    NomeCorrentista = models.CharField(max_length=50)
    TipoOperacao = models.CharField(max_length=7) # 'Crédito' ou 'Débito'
    Descricao = models.CharField(max_length=50)
    DataOperacao = models.DateTimeField()
    ValorOperacao = models.DecimalField(max_digits=15, decimal_places=2)
    BeneficiarioID = models.IntegerField(null=True)
    NomeBeneficiario = models.CharField(max_length=50, null=True)

    class Meta:
     
        managed = False 
        db_table = 'vwExtrato' 
        
        