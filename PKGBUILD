# Maintainer: Joan Bruguera Micó <joanbrugueram@gmail.com>
pkgname=full-offline-backup-for-todoist-git
pkgver=0.1
pkgrel=1
pkgdesc="Small, dependency-less Python script to make a backup of all Todoist tasks and attachments that is accessible offline"
arch=('any')
url="https://github.com/joanbm/full-offline-backup-for-todoist"
license=('GPLv3')
depends=('python' 'python-setuptools')
makedepends=('git' 'python-setuptools')
provides=('full-offline-backup-for-todoist')
conflicts=('full-offline-backup-for-todoist')
options=(!emptydirs)
source=('git+https://github.com/joanbm/full-offline-backup-for-todoist.git')
sha256sums=('SKIP')

pkgver() {
	cd "$srcdir/${pkgname%-git}"
	printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
	cd "$srcdir/${pkgname%-git}"
	python setup.py install --root="$pkgdir/" --optimize=1
}
