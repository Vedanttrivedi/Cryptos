window.cssSelect = (option) => {
    const parent = option.parentNode.parentNode;
    parent.querySelector('[data-css-select="hidden"]').value = option.dataset.cssSelect;
    parent.querySelector('[data-css-select="selected"]').value = option.innerHTML;
    document.activeElement.blur();
  };
  document.addEventListener('mousedown', (event) => {
    const target = event.target;
    if (!(target.dataset.cssSelect && target.dataset.cssSelect === 'selected')) {
        return null;
    }
    if (window.getComputedStyle(target.nextElementSibling).visibility === 'visible') {
        setTimeout(() => void document.activeElement.blur(), 0);
    }
  });