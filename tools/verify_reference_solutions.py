"""Run each task in isolation with its matching reference implementation."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]

def main():
    count=0
    for module in sorted((ROOT/'modules').iterdir()):
        if module.name.startswith('_'): continue
        for kind in ('project','checkpoint'):
            task=module/kind
            if not task.is_dir(): continue
            with tempfile.TemporaryDirectory(prefix='wear-reference-') as temp:
                module_copy=Path(temp)/module.name
                shutil.copytree(module,module_copy,ignore=shutil.ignore_patterns('__pycache__','*.csv','*.png'))
                dest=module_copy/kind
                references=ROOT/'reference_solutions'/module.name
                for source in references.glob('*.py'):
                    if (dest/source.name).exists(): shutil.copy2(source,dest/source.name)
                print(f'Checking {module.name}/{kind}',flush=True)
                # Existing Module 00 tests are pytest functions. New tests use unittest.
                command=[sys.executable,'-m','pytest','-q'] if module.name.startswith('00_') else [sys.executable,'-m','unittest','-v','test_task']
                subprocess.run(command,cwd=dest,check=True)
                count+=1
    print(f'Passed all {count} reference task suites.')

if __name__=='__main__': main()
