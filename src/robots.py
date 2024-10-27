import logging as log
import requests

def robotCheckpoint(domain):

    for protocol in ['https', 'http']:
        paperwork = f'{protocol}://{domain}/robots.txt'

        try:
            response = requests.get(paperwork)
            response.raise_for_status()
            log.info(f'Successfully fetched robots.txt from {paperwork}')
            return response.text
        
        except requests.exceptions.RequestException:
            log.warning(f'Failed to fetch {paperwork}, trying next protocol...')

    log.warning(f'Failed to fetch robots.txt for domain {domain} using both HTTP and HTTPS.')
    return None

def checkPermissions(url):

    domain = url.split('/')[2]
    checkpoint = robotCheckpoint(domain)

    if checkpoint is None:
        log.warning(f"No robots.txt found for {domain}, assuming no restrictions.")
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
    
    log.info('Disallowed paths for domain "%s": %s', domain, ', '.join(disallow_paths) if disallow_paths else 'None')
    return disallow_paths
