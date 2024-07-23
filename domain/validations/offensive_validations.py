# domain/validations/offensive_validations.py
def is_offensive(text):
    offensive_words = [
        'puta', 'puto', 'mierda', 'cabron', 'cabrona', 'idiota', 'imbecil', 'imbécil', 'estupido',
        'estupida', 'pendejo', 'pendeja', 'coño', 'joder', 'gilipollas', 'tonto', 'tonta', 'tarado',
        'marica', 'maricón', 'maricona', 'zorra', 'culero', 'culera', 'polla', 'verga', 'chinga',
        'chingar', 'chupapollas', 'chupapenes', 'malparido', 'malparida', 'hijueputa', 'tarada',
        'hijo de puta', 'perra', 'cabrón', 'cojones', 'culiado', 'forro', 'boludo', 'gil', 'pelotudo',
        'pelotuda', 'pajero', 'pajera', 'vergota', 'chingada', 'chingado', 'chingona', 'chingón',
        'inútil', 'maldito', 'bruto', 'cretino', 'desgraciado', 'asqueroso', 'mamón', 'subnormal',
        'bastardo', 'cabronazo'
    ]

    negative_verbs = [
        'atacar', 'ataco', 'atacas', 'ataca', 'atacamos', 'atacan', 'atacando', 'atacarán', 'atacaría', 
        'maltratar', 'maltrato', 'maltratas', 'maltrata', 'maltratamos', 'maltratan', 'maltratando', 'maltratarán', 'maltrataría', 
        'amenazar', 'amenazo', 'amenazas', 'amenaza', 'amenazamos', 'amenazan', 'amenazando', 'amenazarán', 'amenazaría', 
        'engañar', 'engaño', 'engañas', 'engaña', 'engañamos', 'engañan', 'engañando', 'engañarán', 'engañaría', 
        'robar', 'robo', 'robas', 'roba', 'robamos', 'roban', 'robando', 'robarán', 'robaría', 
        'destruir', 'destruyo', 'destruyes', 'destruye', 'destruimos', 'destruyen', 'destruyendo', 'destruirán', 'destruiría', 
        'golpear', 'golpeo', 'golpeas', 'golpea', 'golpeamos', 'golpean', 'golpeando', 'golpearán', 'golpearía', 
        'matar', 'mato', 'matas', 'mata', 'matamos', 'matan', 'matando', 'matarán', 'mataría', 
        'abusar', 'abuso', 'abusas', 'abusa', 'abusamos', 'abusan', 'abusando', 'abusarán', 'abusaría', 
        'herir', 'hiero', 'hieres', 'hiere', 'herimos', 'hieren', 'hiriendo', 'herirán', 'heriría', 
        'acosar', 'acoso', 'acosas', 'acosa', 'acosamos', 'acosan', 'acosando', 'acosarán', 'acosaría', 
        'humillar', 'humillo', 'humillas', 'humilla', 'humillamos', 'humillan', 'humillando', 'humillarán', 'humillaría', 
        'insultar', 'insulto', 'insultas', 'insulta', 'insultamos', 'insultan', 'insultando', 'insultarán', 'insultaría', 
        'odiar', 'odio', 'odias', 'odia', 'odiamos', 'odian', 'odiando', 'odiarán', 'odiaría', 
        'discriminar', 'discrimino', 'discriminas', 'discrimina', 'discriminamos', 'discriminan', 'discriminando', 'discriminarán', 'discriminaría', 
        'perjudicar', 'perjudico', 'perjudicas', 'perjudica', 'perjudicamos', 'perjudican', 'perjudicando', 'perjudicarán', 'perjudicaría', 
        'sabotear', 'saboteo', 'saboteas', 'sabotea', 'saboteamos', 'sabotean', 'saboteando', 'sabotearán', 'sabotearía', 
        'vengarse', 'me vengo', 'te vengas', 'se venga', 'nos vengamos', 'se vengan', 'vengándose', 'vengarán', 'vengaría', 
        'estafar', 'estafo', 'estafas', 'estafa', 'estafamos', 'estafan', 'estafando', 'estafarán', 'estafaría', 
        'violar', 'violo', 'violas', 'viola', 'violamos', 'violan', 'violando', 'violarán', 'violaría', 
        'extorsionar', 'extorsiono', 'extorsionas', 'extorsiona', 'extorsionamos', 'extorsionan', 'extorsionando', 'extorsionarán', 'extorsionaría', 
        'difamar', 'difamo', 'difamas', 'difama', 'difamamos', 'difaman', 'difamando', 'difamarán', 'difamaría', 
        'secuestrar', 'secuestro', 'secuestras', 'secuestra', 'secuestramos', 'secuestran', 'secuestrando', 'secuestrarán', 'secuestraría', 
        'torturar', 'torturo', 'torturas', 'tortura', 'torturamos', 'torturan', 'torturando', 'torturarán', 'torturaría', 
        'suicidar', 'suicido', 'suicidas', 'suicida', 'suicidamos', 'suicidan', 'suicidando', 'suicidarán', 'suicidaría', 
        'mutilar', 'mutilo', 'mutilas', 'mutila', 'mutilamos', 'mutilan', 'mutilando', 'mutilarán', 'mutilaría', 
        'expulsar', 'expulso', 'expulsas', 'expulsa', 'expulsamos', 'expulsan', 'expulsando', 'expulsarán', 'expulsaría', 
        'asaltar', 'asalto', 'asaltas', 'asalta', 'asaltamos', 'asaltan', 'asaltando', 'asaltarán', 'asaltaría', 
        'extorsionar', 'extorsiono', 'extorsionas', 'extorsiona', 'extorsionamos', 'extorsionan', 'extorsionando', 'extorsionarán', 'extorsionaría', 
        'chantajear', 'chantajeo', 'chantajeas', 'chantajea', 'chantajeamos', 'chantajean', 'chantajeando', 'chantajearán', 'chantajearía', 
        'traficar', 'trafico', 'traficas', 'trafica', 'traficamos', 'trafican', 'traficando', 'traficarán', 'traficaría', 
        'chingar', 'chingo', 'chingas', 'chinga', 'chingamos', 'chingan', 'chingando', 'chingarán', 'chingaría', 
        'incendiar', 'incendio', 'incendias', 'incendia', 'incendiamos', 'incendian', 'incendiando', 'incendiarán', 'incendiaría', 
        'corromper', 'corrompo', 'corrompes', 'corrompe', 'corrompemos', 'corrompen', 'corrompiendo', 'corromperán', 'corrompería', 
        'degradar', 'degrado', 'degradas', 'degrada', 'degradamos', 'degradan', 'degradando', 'degradarán', 'degradaría', 
        'deshonrar', 'deshonro', 'deshonras', 'deshonra', 'deshonramos', 'deshonran', 'deshonrando', 'deshonrarán', 'deshonraría', 
        'despreciar', 'desprecio', 'desprecias', 'desprecia', 'despreciamos', 'desprecian', 'despreciando', 'despreciarán', 'despreciaría', 
        'denigrar', 'denigro', 'denigras', 'denigra', 'denigramos', 'denigran', 'denigrando', 'denigrarán', 'denigraría', 
        'agredir', 'agredo', 'agredes', 'agrede', 'agredimos', 'agreden', 'agrediendo', 'agredirán', 'agrediría', 
        'violentar', 'violento', 'violentas', 'violenta', 'violentamos', 'violentan', 'violentando', 'violentarán', 'violentaría', 
        'mentir', 'miento', 'mientes', 'miente', 'mentimos', 'mienten', 'mintiendo', 'mentirán', 'mentiría', 
        'calumniar', 'calumnio', 'calumnias', 'calumnia', 'calumniamos', 'calumnian', 'calumniando', 'calumniarán', 'calumniaría', 
        'profanar', 'profano', 'profanas', 'profana', 'profanamos', 'profanan', 'profanando', 'profanarán', 'profanaría', 
        'desfigurar', 'desfiguro', 'desfiguras', 'desfigura', 'desfiguramos', 'desfiguran', 'desfigurando', 'desfigurarán', 'desfiguraría',
        'esclavizar', 'esclavizo', 'esclavizas', 'esclaviza', 'esclavizamos', 'esclavizan', 'esclavizando', 'esclavizarán', 'esclavizaría', 
        'explotar', 'exploto', 'explotas', 'explota', 'explotamos', 'explotan', 'explotando', 'explotarán', 'explotaría', 
        'coaccionar', 'coacciono', 'coaccionas', 'coacciona', 'coaccionamos', 'coaccionan', 'coaccionando', 'coaccionarán', 'coaccionaría', 
        'engendrar', 'engendro', 'engendras', 'engendra', 'engendramos', 'engendran', 'engendrando', 'engendrarán', 'engendraría', 
        'envenenar', 'enveneno', 'envenenas', 'envenena', 'envenenamos', 'envenenan', 'envenenando', 'envenenarían', 'envenenaría', 
        'enfurecer', 'enfurezco', 'enfureces', 'enfurece', 'enfurecemos', 'enfurecen', 'enfureciendo', 'enfurecerán', 'enfurecería', 
        'alienar', 'alieno', 'alienas', 'aliena', 'alienamos', 'alienan', 'alienando', 'alienarán', 'alienaría', 
        'despojar', 'despojo', 'despojas', 'despoja', 'despojamos', 'despojan', 'despojando', 'despojarán', 'despojaría', 
        'excluir', 'excluyo', 'excluyes', 'excluye', 'excluimos', 'excluyen', 'excluyendo', 'excluirán', 'excluiría', 
        'erradicar', 'erradico', 'erradicas', 'erradica', 'erradicamos', 'erradican', 'erradicando', 'erradicarán', 'erradicaría', 
        'deshumanizar', 'deshumanizo', 'deshumanizas', 'deshumaniza', 'deshumanizamos', 'deshumanizan', 'deshumanizando', 'deshumanizarán', 'deshumanizaría', 
        'desacreditar', 'desacredito', 'desacreditas', 'desacredita', 'desacreditamos', 'desacreditan', 'desacreditando', 'desacreditarán', 'desacreditaría', 
        'abofetear', 'abofeteo', 'abofeteas', 'abofetea', 'abofeteamos', 'abofetean', 'abofeteando', 'abofetearán', 'abofetearía', 
        'subyugar', 'subyugo', 'subyugas', 'subyuga', 'subyugamos', 'subyugan', 'subyugando', 'subyugarán', 'subyugaría', 
    ]

    text = text.lower()
    combined_list = offensive_words + negative_verbs
    for word in combined_list:
        if word in text:
            return True
    return False

def validate_offensive_content(text, field_name):
    if is_offensive(text):
        raise ValueError(f"{field_name} contiene contenido ofensivo o inapropiado.")
