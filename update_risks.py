from bs4 import BeautifulSoup
from pathlib import Path
p=Path('/mnt/data/iglu_latest/iglu_revision/index.html')
soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
slides=soup.select('section.slide')
old=next(s for s in slides if s.get('data-title')=='Risks')
risks=[
('Inaccurate or incomplete requirements','Business processes may be misunderstood.','Consult IGLÚ representatives and validate employee, attendance, pricing, discount, and transaction rules.'),
('Scope creep','Additional features may exceed the approved scope and schedule.','Maintain the approved scope. Record additional requests as possible future enhancements.'),
('Schedule delays','Academic and personal responsibilities may affect deadlines.','Use ClickUp to assign tasks, set deadlines, monitor progress, and hold regular meetings.'),
('Technical difficulties','Issues may occur in databases, access controls, calculations, or responsive design.','Plan early, develop core features first, test incrementally, and use GitHub for version control.'),
('Internet connectivity issues','Poor connection may prevent system access or saving records.','Use stable internet and mobile data as backup. Offline transaction processing is excluded.'),
('Data entry errors','Incorrect employee, attendance, product, price, or transaction records.','Apply input validation, confirmation screens, and authorized record reviews. Use test data during development.'),
('Unauthorized access or modification','Users may access or alter restricted records.','Implement secure login, role-based permissions, session controls, and audit logs.'),
('Data loss','Files or records may be lost through errors or system issues.','Use GitHub, maintain document and database backups, and prepare a recovery procedure.'),
('Limited budget or unexpected expenses','Costs may exceed the ₱3,410 estimate.','Prioritize free tools, record expenses, review purchases, and use the contingency fund only for documented needs.'),
('Free hosting or database limitations','Storage, reliability, or security may be inadequate.','Evaluate service limits and backup options. Seek approval before using paid services.'),
('Low user adoption','Employees may find the system unfamiliar or difficult.','Provide a simple responsive interface, role-based accounts, orientation, and user feedback.'),
('Device or browser compatibility','The system may not work properly on available devices.','Test common desktop and mobile browsers and resolve major compatibility issues.'),
('Delayed client feedback','Unavailable representatives may delay validation and testing.','Schedule consultations early, set feedback deadlines, prepare questions, and document decisions.'),
('Insufficient testing','Undetected errors may affect system reliability.','Test attendance, calculations, discounts, payments, permissions, transaction reviews, and audit logs before pilot implementation.')]

def make_slide(part, items, number):
    sec=soup.new_tag('section', attrs={'class':'slide risk-detail-slide','data-title':f'Possible Risks {part}'})
    head=soup.new_tag('header',attrs={'class':'slide-head'})
    kicker=soup.new_tag('span',attrs={'class':'slide-kicker'}); kicker.string=f'{number:02d}'
    h=soup.new_tag('h2'); h.string=f'Possible Risks and Proposed Solutions ({part}/3)'
    tag=soup.new_tag('span',attrs={'class':'part-tag'}); tag.string='Risk assessment and mitigation measures from the project proposal'
    head.extend([kicker,h,tag]); sec.append(head)
    grid=soup.new_tag('div',attrs={'class':'risk-detail-grid'})
    for idx,(name,desc,solution) in items:
        card=soup.new_tag('article',attrs={'class':'risk-detail-card'})
        top=soup.new_tag('div',attrs={'class':'risk-detail-top'})
        num=soup.new_tag('span',attrs={'class':'risk-number'}); num.string=f'{idx:02d}'
        title=soup.new_tag('h3'); title.string=name
        top.extend([num,title]); card.append(top)
        label=soup.new_tag('span',attrs={'class':'risk-label'}); label.string='POSSIBLE RISK'
        para=soup.new_tag('p',attrs={'class':'risk-description'}); para.string=desc
        solution_box=soup.new_tag('div',attrs={'class':'risk-solution'})
        slabel=soup.new_tag('span',attrs={'class':'solution-label'}); slabel.string='PROPOSED SOLUTION'
        sp=soup.new_tag('p'); sp.string=solution
        solution_box.extend([slabel,sp])
        card.extend([label,para,solution_box]); grid.append(card)
    sec.append(grid)
    return sec

# Replace original one-slide summary with three source-faithful slides.
newslides=[make_slide('1',list(enumerate(risks[:5],1)),10),
           make_slide('2',list(enumerate(risks[5:9],6)),11),
           make_slide('3',list(enumerate(risks[9:],10)),12)]
old.replace_with(newslides[0]); newslides[0].insert_after(newslides[1]); newslides[1].insert_after(newslides[2])
# Renumber visible slide markers to match their new positions (title slide has no marker).
for idx,sec in enumerate(soup.select('section.slide'),1):
    marker=sec.select_one('.slide-kicker')
    if marker: marker.string=f'{idx:02d}'
# Set meaningful title attributes and preserve the 3-part labels.
for sec,part in zip(newslides,['1','2','3']):
    h=sec.select_one('h2')
    h.string=f'Possible Risks and Proposed Solutions ({part}/3)'
    sec['data-title']=f'Possible Risks ({part}/3)'
# Add slide number to section data order is managed by JS.
p.write_text(str(soup),encoding='utf-8')
