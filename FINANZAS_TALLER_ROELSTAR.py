import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title='ROELSTAR | Finanzas de Taller', page_icon='⭐', layout='wide', initial_sidebar_state='collapsed')
NAVY='#08245B'; RED='#C90000'; GREEN='#00B050'; YELLOW='#FFFF00'; GRAY='#D9D9D9'
st.markdown(f'''<style>
.block-container{{padding-top:1.5rem;max-width:1700px}}
.rs-title{{font-size:1.8rem;font-weight:800;color:{NAVY}}}.rs-sub{{color:#596273;margin-bottom:1rem}}
.rs-table{{width:100%;border-collapse:collapse;font-size:11px;table-layout:fixed}}
.rs-table th,.rs-table td{{border:1px solid #c7cbd1;padding:5px 3px;text-align:right;overflow-wrap:anywhere}}
.rs-table th:first-child,.rs-table td:first-child{{text-align:left;width:38%}}
.rs-table th{{background:{NAVY};color:white;font-weight:700}}
.rs-table .income{{background:#E2F0D9}}.rs-table .total{{font-weight:800;background:#D9E2F3}}
.rs-table .cost{{background:#FFF2CC}}.rs-table .utility{{background:{YELLOW}}}.rs-table .margin{{background:{GRAY}}}
div[data-testid="stNumberInput"] input{{text-align:right}}
</style>''', unsafe_allow_html=True)
# Encabezado con el logo real de ROELSTAR.
logo_path = Path(__file__).with_name('roelstar_logo.png')
head_logo, head_title = st.columns([1, 6], vertical_alignment='center')
with head_logo:
    if logo_path.exists():
        st.image(str(logo_path), width=145)
    else:
        st.markdown('⭐ **ROELSTAR**')
with head_title:
    st.markdown('<div class="rs-title">FINANZAS DE TALLER</div><div class="rs-sub">Estado de resultados mensual · cifras expresadas en millones de pesos (COP)</div>', unsafe_allow_html=True)

# Entradas visibles en la página principal.
st.markdown('### 🟩 Datos de entrada')
st.caption('Escriba en los campos de entrada; totales, utilidades y márgenes se calculan automáticamente.')
tab_real, tab_bud = st.tabs(['Resultados del mes', 'Presupuesto del mes'])
with tab_real:
    st.markdown('**Resultados reales del mes · millones de COP**')
    ir1, ir2, ir3 = st.columns(3)
    with ir1:
        real_mec = st.number_input( 'B7 · Ingreso M.O. MEC', min_value=0.0, value=0.0, step=0.1, format='%.3f', key='real_mec')
    with ir2:
        real_col = st.number_input('C7 · Ingreso M.O. COL', min_value=0.0, value=0.0, step=0.1, format='%.3f', key='real_col')
    with ir3:
        real_rptos = st.number_input('D7 · Ingreso M.O. RPTOS', min_value=0.0, value=0.0, step=0.1, format='%.3f', key='real_rptos')
with tab_bud:
    st.markdown('**Presupuesto del mes · millones de COP**')
    ib1, ib2, ib3 = st.columns(3)
    with ib1:
        bud_mec_mo = st.number_input('G7 · Ingreso M.O. MEC', min_value=0.0, value=72.2, step=0.1, format='%.3f', key='bud_mec_mo')
        bud_mec_rptos = st.number_input('G8 · Ingreso repuestos MEC', min_value=0.0, value=90.2, step=0.1, format='%.3f', key='bud_mec_rptos')
        bud_mec_tot = st.number_input('G9 · Ingreso TOT MEC', min_value=0.0, value=3.0, step=0.1, format='%.3f', key='bud_mec_tot')
        bud_col_cost_mo = st.number_input('H13 · Costo M.O. COL', min_value=0.0, value=55.0, step=0.1, format='%.3f', key='bud_col_cost_mo')
    with ib2:
        bud_col_mo = st.number_input('H7 · Ingreso M.O. COL', min_value=0.0, value=95.3, step=0.1, format='%.3f', key='bud_col_mo')
        bud_col_cost_rptos = st.number_input('H14 · Costo repuestos COL', min_value=0.0, value=124.2, step=0.1, format='%.3f', key='bud_col_cost_rptos')
        bud_col_mat = st.number_input('H10 · Ingreso materiales e insumos COL', min_value=0.0, value=5.8, step=0.1, format='%.3f', key='bud_col_mat')
    with ib3:
        bud_rptos_rptos = st.number_input('I8 · Ingreso repuestos RPTOS', min_value=0.0, value=99.1, step=0.1, format='%.3f', key='bud_rptos_rptos')
        bud_rptos_cost_rptos = st.number_input('I14 · Costo repuestos RPTOS', min_value=0.0, value=65.0, step=0.1, format='%.3f', key='bud_rptos_cost_rptos')
        bud_col_cost_mat = st.number_input('H16 · Costo materiales e insumos COL', min_value=0.0, value=4.2, step=0.1, format='%.3f', key='bud_col_cost_mat')

def calc(real=True):
    if real:
        b7,c7,d7=real_mec,real_col,real_rptos
        b8,c8,d8=b7*1.3,c7*1.9,(b7*1.3+c7*1.9)*.45
        b9,c9,d9=b7*.03,c7*.06,0.0
        b10,c10,d10=b9/3,c7*.065,0.0
        b13,c13,d13=b7*.4,c7*.6,0.0
        b14,c14,d14=b8*.71,c8*.78,d8*.69
        b15,c15,d15=b9*.7,c9*.85,0.0
        b16,c16,d16=b10*.71,c10*.63,0.0
    else:
        b7,c7,d7=bud_mec_mo,bud_col_mo,0.0
        b8,c8,d8=bud_mec_rptos,c7*1.9,bud_rptos_rptos
        b9,c9,d9=bud_mec_tot,c7*.06,0.0
        b10,c10,d10=b9/3,bud_col_mat,0.0
        b13,c13,d13=b7*.4,bud_col_cost_mo,0.0
        b14,c14,d14=b8*.71,bud_col_cost_rptos,bud_rptos_cost_rptos
        b15,c15,d15=b9*.7,c9*.85,0.0
        b16,c16,d16=b10*.71,bud_col_cost_mat,0.0
    rows={}
    for r,v in [(7,[b7,c7,d7]),(8,[b8,c8,d8]),(9,[b9,c9,d9]),(10,[b10,c10,d10]),(13,[b13,c13,d13]),(14,[b14,c14,d14]),(15,[b15,c15,d15]),(16,[b16,c16,d16])]: rows[r]=v+[sum(v)]
    rows[11]=[sum(rows[r][i] for r in [7,8,9,10]) for i in range(4)]
    rows[17]=[sum(rows[r][i] for r in [13,14,15,16]) for i in range(4)]
    for r,inc,cost in [(19,7,13),(20,8,14),(21,9,15),(22,10,16)]: rows[r]=[rows[inc][i]-rows[cost][i] for i in range(4)]
    rows[23]=[sum(rows[r][i] for r in [19,20,21,22]) for i in range(4)]
    for r,profit,inc in [(25,19,7),(26,20,8),(27,21,9),(28,22,10),(29,23,11)]: rows[r]=[rows[profit][i]/rows[inc][i] if rows[inc][i] else 0.0 for i in range(4)]
    return rows

real=calc(True); budget=calc(False); variance={r:[real[r][i]-budget[r][i] for i in range(4)] for r in real}
labels={7:'Ingreso M.O.',8:'Ingreso Rptos',9:'Ingreso TOT',10:'Ingreso Mat. & Insumos',11:'INGRESOS',13:'Costo M.O.',14:'Costo Rptos',15:'Costo TOT',16:'Costo Mat. & Insumos',17:'COSTO VENTAS',19:'Utilidad Bruta M.O.',20:'Utilidad Bruta Rptos',21:'Utilidad Bruta TOT',22:'Utilidad Bruta Mat. & Insumos',23:'UTILIDAD BRUTA',25:'% Margen M.O.',26:'% Margen Rptos',27:'% Margen TOT',28:'% Margen Mat. & Insumos',29:'% Margen Total'}
def fmt(v,pct=False):
    if pct: return f'{v*100:.1f}%'.replace('.',',')
    if abs(v)<0.0005:return '-'
    s=f'{abs(v):.1f}'.replace('.',',')
    return f'({s})' if v<0 else s
def html_table(title, cols, data, typ):
    head=NAVY if typ=='real' else RED
    out=f'<div style="border:1px solid #bcc3ce;border-radius:4px;overflow:hidden"><div style="background:{head};color:white;text-align:center;font-weight:bold;padding:7px;font-size:13px">{title}</div><table class="rs-table"><tr><th>Rubro</th>'+''.join(f'<th>{c}</th>' for c in cols)+'</tr>'
    for r,label in labels.items():
        cl='income' if r in [7,8,9,10] else 'total' if r in [11,17] else 'utility' if r in [19,20,21,22,23] else 'margin'
        if typ=='variance' and r in [19,20,21,22,23]:cl='utility'
        out+=f'<tr class="{cl}"><td>{label}</td>'+''.join(f'<td>{fmt(v,r>=25)}</td>' for v in data[r])+'</tr>'
    return out+'</table></div>'

st.markdown('### Estado de resultados')
a,b,c=st.columns(3,gap='small')
with a: st.markdown(html_table('RESULTADOS MES',['MEC','COL','RPTOS','TOTAL'],real,'real'),unsafe_allow_html=True)
with b: st.markdown(html_table('PRESUPUESTO MES',['MEC','COL','RPTOS','TOTAL'],budget,'budget'),unsafe_allow_html=True)
with c: st.markdown(html_table('RESULTADO VS. PRESUPUESTO',['MEC','COL','RPTOS','TOTAL'],variance,'variance'),unsafe_allow_html=True)

st.markdown('### EL GERENTE QUISIERA SABER')
rev=real[11]; profits=real[23]; units=['MEC','COL','RPTOS']; shares=[rev[i]/rev[3] if rev[3] else 0 for i in range(3)]
if rev[3]:
    idx=max(range(3),key=lambda i:shares[i]); top=units[idx]
    margin_data=[(units[i],profits[i]/rev[i] if rev[i] else 0) for i in range(3)]; best=max(margin_data,key=lambda z:z[1])[0]
else: top=best='sin datos'
share_top = shares[units.index(top)] if top in units else 0.0
answers=[
 (f'{top} aporta la mayor participación de ingresos ({fmt(share_top,True)}). Su peso influye directamente en el resultado total.' if top in units else 'Aún no hay ingresos reales para identificar la unidad con mayor participación. Ingrese los datos del mes para calcularlo.'),
 f'Con los resultados actuales, {best} tiene el mayor margen bruto relativo. La decisión también debe considerar utilidad absoluta y participación en ventas.',
 'Compare el margen porcentual y la utilidad absoluta de mano de obra y repuestos; ventas altas no garantizan mayor utilidad si el costo también es alto.',
 'Concentre esfuerzos en las líneas que combinen margen favorable, capacidad operativa y oportunidad real de aumentar la utilidad bruta.',
 f'La variación de utilidad bruta total frente al presupuesto es {fmt(variance[23][3])} millones. Revise las diferencias de ingresos y costos por unidad.',
 'COL puede vender más y ganar menos si los costos crecen más que los ingresos o si cambia la mezcla de servicios y materiales vendidos.',
 'El crecimiento en repuestos es rentable si la utilidad bruta y el margen mejoran, no solo si aumenta la facturación.',
 f'La unidad con mayor margen relativo calculado es {best}; antes de invertir, contraste también su utilidad absoluta y potencial de crecimiento.',
 'Controle semanalmente descuentos, costo de repuestos, productividad de mano de obra y desviaciones presupuestales; asigne responsables y fechas de acción.'
]
questions=['1. ¿Qué unidad genera mayor participación en ingresos y qué impacto tiene?','2. ¿Cuál unidad es más rentable según los indicadores?','3. ¿Qué diferencia hay entre la rentabilidad de mano de obra y repuestos?','4. ¿En qué línea enfocaría esfuerzos para aumentar la utilidad bruta?','5. ¿Por qué la utilidad bruta quedó por debajo del presupuesto?','6. ¿Por qué COL puede superar ventas y no alcanzar la utilidad esperada?','7. ¿El crecimiento de repuestos está siendo rentable?','8. ¿En qué unidad invertiría más recursos?','9. ¿Qué acción mejoraría el margen bruto y el cumplimiento del presupuesto?']
for q,ans in zip(questions,answers):
    with st.expander(q): st.write(ans if rev[3] or q.startswith(('6.','7.','9.')) else 'Ingrese los resultados reales del mes para que el análisis se base en datos y no en supuestos.')

rows=[]
for r,label in labels.items():
    rows.append({'Rubro':label,**{f'Real {u}':real[r][i] for i,u in enumerate(['MEC','COL','RPTOS','TOTAL'])},**{f'Presupuesto {u}':budget[r][i] for i,u in enumerate(['MEC','COL','RPTOS','TOTAL'])},**{f'Variación {u}':variance[r][i] for i,u in enumerate(['MEC','COL','RPTOS','TOTAL'])}})
st.download_button('Descargar resultados en CSV',pd.DataFrame(rows).to_csv(index=False).encode('utf-8-sig'),'roelstar_resultados.csv','text/csv')
st.caption('Resultado vs. presupuesto = resultado real − presupuesto. Si el denominador de un margen es cero, se muestra 0,0 % para evitar #DIV/0!.')
