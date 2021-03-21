import time
from subprocess import check_call
from subprocess import check_output
from subprocess import CalledProcessError
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


# Chemins configurables
git_path = 'C:/Program Files (x86)/Git/bin/git.exe'
repo_path = 'W:/zim'
ac_branch = 'autocommit'

# Délais minimums en secondes.
commit_delay = 5
push_delay = 360  # Doit être un multiple de commit_delay.

# Utiliser l'authentification par nom d'utilisateur et mot de passe.
# Lecture à partir d'un fichier pour éviter le partage en ligne des sources ouvertes.
with open('x.txt', 'r') as cf:
    # https://username:password@host/username/repo.git
    username_password_at_host_username_repo = cf.read()

changed_detected = False
new_commits = False


class DirModifiedCommitHandler(PatternMatchingEventHandler):
    """Gère les événements de modification, en ignorant le répertoire git."""

    def __init__(self):
        PatternMatchingEventHandler.__init__(self, ignore_patterns=['*\.git*'])

    def on_modified(self, event):
        print('\n### Changement détecté dans\n ' + event.src_path)
        global changed_detected
        changed_detected = True


def push():
    """ Pousse sur la branche de suivi du même nom."""
    global new_commits
    new_commits = False
    push_cmd = git_path + ' push ' + username_password_at_host_username_repo + ' ' + ac_branch + ' -u'
    check_call(push_cmd, cwd=repo_path)


def commit(retry=False):
    """ Passe à la branche autocommit et commet tous les changements."""
    print('## Starting commit.')
    now = str(time.time())

    # Git commandes
    addcmd = git_path + " add -A"
    check_if_commit_is_needed = git_path + ' diff-index --quiet HEAD'
    commit_cmd = git_path + " commit -a -m 'autocommit:" + now + "'"
    get_branch_name = git_path + " symbolic-ref --short -q HEAD"
    reset = git_path + ' reset'
    switch_without_changing_working_dir = git_path + ' symbolic-ref HEAD refs/heads/' + ac_branch
    check_branch_exists = git_path + ' rev-parse --verify ' + ac_branch  # 0 return code for success.
    create_branch = git_path + ' checkout -b ' + ac_branch

    # Changer ou créer une branche.
    # C'est fait d'une manière qui n'affecte pas l'arbre de travail.
    # Cela a pour résultat de transformer la branche autocommit en l'état de travail actuel.
    # Si vous passez manuellement à une autre branche, ce script est mis en pause.
    # Décoder parce que ses octets ne sont pas unicode, et aussi enlever la nouvelle ligne.
    actual_branch = check_output(get_branch_name, cwd=repo_path).decode('ascii').strip()
    if actual_branch != ac_branch:
        print('## PAUSÉ : SUR UNE MAUVAISE BRANCHE')
        if input('## Voulez-vous changer de branche ou réessayer maintenant ? (y/n)?') != 'y':
            print('## Tentative de validation avortée..')
            commit()
            return
        try:
            check_call(check_branch_exists, cwd=repo_path)
        except CalledProcessError:
            check_call(create_branch, cwd=repo_path)
        try:
            check_call(switch_without_changing_working_dir, cwd=repo_path)
            check_call(reset, cwd=repo_path)
        except CalledProcessError:
            print('## Échec du changement de branche, abandon.')
            raise SystemExit(1)

    # Essayez d'ajouter tout.
    try:
        check_call(addcmd, cwd=repo_path)
    except CalledProcessError:
        print('## Ajout a échoué.')
        if not retry:
            print('## ...réessayer.')
            time.sleep(5)
            commit(True)
            return  # La nouvelle tentative fera le commit.

    # Vérifier s'il y a quelque chose à commettre puis commettre.
    try:
        check_call(check_if_commit_is_needed, cwd=repo_path)
        print('## Rien à engager.')
    except CalledProcessError:
        # C'est le bloc d'engagement.
        try:
            check_call(commit_cmd, cwd=repo_path)
        except CalledProcessError:
            print('## Engagement a échoué.')
            if not retry:
                print('# ...réessayer.')
                time.sleep(2)
                commit(True)
        finally:
            # Marquer le nouveau commit après sa réalisation.
            # Ceci permet d'éviter qu'un commit soit fait avec un code d'erreur (TODO : est-ce possible ?).
            global new_commits
            new_commits = True

    print('## Tentative, engagement terminée.')


def start():
    # Commencez par un commit, gérez tout changement de branche nécessaire.
    commit()

    global changed_detected
    # Configurer le moniteur de répertoire.
    ev_handler = DirModifiedCommitHandler()
    observer = Observer()
    observer.schedule(ev_handler, repo_path, recursive=True)
    observer.start()

    try:
        counter = 0
        while True:
            time.sleep(commit_delay)
            counter += commit_delay
            if changed_detected:
                changed_detected = False
                commit()
            if counter >= push_delay:
                counter = 0
                if new_commits:
                    push()

    except (KeyboardInterrupt, SystemExit):
        observer.stop()
        raise


start()
