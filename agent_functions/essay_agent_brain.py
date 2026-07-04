from agent_functions import research_agent, drafting_agent, Editing_agent, YES_or_No_agent

def create_and_really_good_essay(query):
    research_agent.research(query)
    correction_cycle(query)

def correction_cycle(query):
    cc = 3
    is_correction = False
    while cc > 0:
        drafting_agent.draft_the_information(query, is_correction_cycle=is_correction)
        Editing_agent.edit_the_essay()
        
        is_approved = YES_or_No_agent.yes_or_no(query)
        if is_approved:
            break
            
        cc -= 1
        is_correction = True
