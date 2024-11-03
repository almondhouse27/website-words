import logging as log
import requests

###--------------------------------->>>>>>>
# 
def robotCheckpoint(domain, ROBOT_RETRY):

    for protocol in ['https', 'http']:
        paperwork = f'{protocol}://{domain}/robots.txt'

        # try:
        #     response = requests.get(paperwork)
        #     response.raise_for_status()
        #     log.info(f'R- Successfully read robots.txt from {paperwork}')
        #     print(log.info(f'R- Successfully read robots.txt from {paperwork}'))
        #     return response.text
        
        # except requests.exceptions.RequestException:
        #     log.warning(f'R- Failed to find {paperwork}, trying next protocol...')
        #     print(f'R- Failed to find {paperwork}, trying next protocol...')

        for attempt in range(ROBOT_RETRY):
            try:
                response = requests.get(paperwork, timeout=5)
                response.raise_for_status()  # Raise an error for bad responses
                log.info(f'R- Successfully read robots.txt from {paperwork}')
                return response.text
            
            except requests.exceptions.Timeout:
                log.warning(f'R- Timeout occurred while fetching {paperwork}. Attempt {attempt + 1} of {ROBOT_RETRY}.')
                if attempt + 1 == ROBOT_RETRY:
                    log.warning(f'R- Giving up on {paperwork} after {ROBOT_RETRY} attempts.')
                    #print(f'R- Giving up on {paperwork} after {ROBOT_RETRY} attempts.')
            
            except requests.exceptions.RequestException as e:
                log.warning(f'R- Failed to find {paperwork}: {e}, trying next protocol...')
                break   

    log.warning(f'R- Failed to obtain robots.txt for domain {domain} using both HTTP and HTTPS.')
    #print(f'R- Failed to obtain robots.txt for domain {domain} using both HTTP and HTTPS.')
    return None


###--------------------------------->>>>>>>
# 
def checkPermissions(url, ROBOT_RETRY):
    domain = url.split('/')[2]
    checkpoint = robotCheckpoint(domain, ROBOT_RETRY)

    if checkpoint is None:
        log.warning(f'R- No robots.txt found for {domain}, assuming no restrictions.')
        #print(f'R- No robots.txt found for {domain}, assuming no restrictions.')
        return[]
        
    rules = checkpoint.splitlines()
    user_agent = '*'
    disallow_paths = []

    for line in rules:
        line = line.strip()

        if line.startswith('User-agent:'):
            user_agent = line.split(':')[1].strip()
        
        elif line.startswith('Disallow:'):
            if user_agent =='*':
                disallow_paths.append(line.split(':')[1].strip())
    
    log.info('R- Disallowed paths for domain %s: %s', domain, ', '.join(disallow_paths) if disallow_paths else 'None')
    #print('R- Disallowed paths for domain %s: %s', domain, ', '.join(disallow_paths) if disallow_paths else 'None')
    return disallow_paths
