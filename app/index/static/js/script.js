jQuery(document).ready(function($) {
    var $side_menu_trigger = $('#nav-trigger'),
      $content_wrapper = $('.main-content'),
      $navigation = $('header');
  
    //open-close lateral menu clicking on the menu icon
    $side_menu_trigger.on('click', function(event) {
      event.preventDefault();
  
      $side_menu_trigger.toggleClass('is-clicked');
      $navigation.toggleClass('menu-open');
      $content_wrapper.toggleClass('menu-open').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function() {
        // firefox transitions break when parent overflow is changed, so we need to wait for the end of the trasition to give the body an overflow hidden
        $('body').toggleClass('overflow-hidden');
      });
      $('#side-nav').toggleClass('menu-open');
  
      //check if transitions are not supported - i.e. in IE9
      if ($('html').hasClass('no-csstransitions')) {
        $('body').toggleClass('overflow-hidden');
      }
    });
  
    //close lateral menu clicking outside the menu itself
    $content_wrapper.on('click', function(event) {
      if (!$(event.target).is('#menu-trigger, #menu-trigger span')) {
        $side_menu_trigger.removeClass('is-clicked');
        $navigation.removeClass('menu-open');
        $content_wrapper.removeClass('menu-open').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function() {
          $('body').removeClass('overflow-hidden');
        });
        $('#side-nav').removeClass('menu-open');
        //check if transitions are not supported
        if ($('html').hasClass('no-csstransitions')) {
          $('body').removeClass('overflow-hidden');
        }
  
      }
    });
  
    //open (or close) submenu items in the lateral menu. Close all the other open submenu items.
    $('.item-has-children').children('a').on('click', function(event) {
      event.preventDefault();
      $(this).toggleClass('submenu-open').next('.sub-menu').slideToggle(200).end().parent('.item-has-children').siblings('.item-has-children').children('a').removeClass('submenu-open').next('.sub-menu').slideUp(200);
    });
  });



  $(".action-button > i").bind("webkitAnimationEnd mozAnimationEnd animationEnd", function(){
    $(this).removeClass("pop-up")  
  });
  
  $(".action-button").mouseenter(function(){
    $(this).find('i').addClass("pop-up");        
  });
  
  //Toggle card shadow
  $('.card').hover(function (){
    $(this).toggleClass('shadow');
  });
  
  //Hover card animation
  $('.hover-name').hover(function() {
    $(this).find('.info-card').addClass('show');
  }, function() {
    $('.info-card').removeClass('show');
  })
  
  //Follow button functions
  $('.follow, .unfollow').on('click', function(e){
    e.preventDefault();
    var el = $(this);
  
    var loader = $('<i>', {
      class: 'fas fa-spinner fa-spin'
    });
    
    el.html(loader);
    
    var btnClass, btnText;
    if(el.hasClass('unfollow')) {
      btnClass = 'follow btn btn-outline-primary font-weight-bold';
      btnText = 'Follow'
    } else {
      btnClass = 'unfollow btn btn-outline-danger font-weight-bold';
      btnText = 'Unfollow'
    }
    
    setTimeout(function(){
      el
      .html(btnText)
      .attr('class', btnClass);
    }, 1000);
  });
  
  // Button Animation
  $('.action-button').on('click', function(){
    var el = $(this);
    el.find('i').toggleClass('pop-up');
    
    if(el.hasClass('retweet')) {
      el.toggleClass('rt-active');
    }
    
    if(el.hasClass('heart')) {
      el.toggleClass('ht-active');
      el.find('i').toggleClass('far fas');
    }
  });



  $(function(){
    $('.product-card').hover(function() {
       $(this).find('.description').animate({
         height: "toggle",
         opacity: "toggle"
       }, 300);
     });
  });





  // ADD recipe script



  var Modal = (function() {

    var trigger = $qsa('.modal__trigger'); // what you click to activate the modal
    var modals = $qsa('.modal'); // the entire modal (takes up entire window)
    var modalsbg = $qsa('.modal__bg'); // the entire modal (takes up entire window)
    var content = $qsa('.modal__content'); // the inner content of the modal
      var closers = $qsa('.modal__close'); // an element used to close the modal
    var w = window;
    var isOpen = false;
      var contentDelay = 400; // duration after you click the button and wait for the content to show
    var len = trigger.length;
  
    // make it easier for yourself by not having to type as much to select an element
    function $qsa(el) {
      return document.querySelectorAll(el);
    }
  
    var getId = function(event) {
  
      event.preventDefault();
      var self = this;
      // get the value of the data-modal attribute from the button
      var modalId = self.dataset.modal;
      var len = modalId.length;
      // remove the '#' from the string
      var modalIdTrimmed = modalId.substring(1, len);
      // select the modal we want to activate
      var modal = document.getElementById(modalIdTrimmed);
      // execute function that creates the temporary expanding div
      makeDiv(self, modal);
    };
  
    var makeDiv = function(self, modal) {
  
      var fakediv = document.getElementById('modal__temp');
  
      /**
       * if there isn't a 'fakediv', create one and append it to the button that was
       * clicked. after that execute the function 'moveTrig' which handles the animations.
       */
  
      if (fakediv === null) {
        var div = document.createElement('div');
        div.id = 'modal__temp';
        self.appendChild(div);
        moveTrig(self, modal, div);
      }
    };
  
    var moveTrig = function(trig, modal, div) {
      var trigProps = trig.getBoundingClientRect();
      var m = modal;
      var mProps = m.querySelector('.modal__content').getBoundingClientRect();
      var transX, transY, scaleX, scaleY;
      var xc = w.innerWidth / 2;
      var yc = w.innerHeight / 2;
  
      // this class increases z-index value so the button goes overtop the other buttons
      trig.classList.add('modal__trigger--active');
  
      // these values are used for scale the temporary div to the same size as the modal
      scaleX = mProps.width / trigProps.width;
      scaleY = mProps.height / trigProps.height;
  
      scaleX = scaleX.toFixed(3); // round to 3 decimal places
      scaleY = scaleY.toFixed(3);
  
  
      // these values are used to move the button to the center of the window
      transX = Math.round(xc - trigProps.left - trigProps.width / 2);
      transY = Math.round(yc - trigProps.top - trigProps.height / 2);
  
          // if the modal is aligned to the top then move the button to the center-y of the modal instead of the window
      if (m.classList.contains('modal--align-top')) {
        transY = Math.round(mProps.height / 2 + mProps.top - trigProps.top - trigProps.height / 2);
      }
  
  
          // translate button to center of screen
          trig.style.transform = 'translate(' + transX + 'px, ' + transY + 'px)';
          trig.style.webkitTransform = 'translate(' + transX + 'px, ' + transY + 'px)';
          // expand temporary div to the same size as the modal
          div.style.transform = 'scale(' + scaleX + ',' + scaleY + ')';
          div.style.webkitTransform = 'scale(' + scaleX + ',' + scaleY + ')';
  
  
          window.setTimeout(function() {
              window.requestAnimationFrame(function() {
                  open(m, div);
              });
          }, contentDelay);
  
    };
  
    var open = function(m, div) {
  
      if (!isOpen) {
        // select the content inside the modal
        var content = m.querySelector('.modal__content');
        // reveal the modal
        m.classList.add('modal--active');
        // reveal the modal content
        content.classList.add('modal__content--active');
  
        /**
         * when the modal content is finished transitioning, fadeout the temporary
         * expanding div so when the window resizes it isn't visible ( it doesn't
         * move with the window).
         */
  
        content.addEventListener('transitionend', hideDiv, false);
  
        isOpen = true;
      }
  
      function hideDiv() {
        // fadeout div so that it can't be seen when the window is resized
        div.style.opacity = '0';
        content.removeEventListener('transitionend', hideDiv, false);
      }
    };
  
    var close = function(event) {
  
          event.preventDefault();
      event.stopImmediatePropagation();
  
      var target = event.target;
      var div = document.getElementById('modal__temp');
  
      /**
       * make sure the modal__bg or modal__close was clicked, we don't want to be able to click
       * inside the modal and have it close.
       */
  
      if (isOpen && target.classList.contains('modal__bg') || target.classList.contains('modal__close')) {
  
        // make the hidden div visible again and remove the transforms so it scales back to its original size
        div.style.opacity = '1';
        div.removeAttribute('style');
  
              /**
              * iterate through the modals and modal contents and triggers to remove their active classes.
        * remove the inline css from the trigger to move it back into its original position.
              */
  
              for (var i = 0; i < len; i++) {
                  modals[i].classList.remove('modal--active');
                  content[i].classList.remove('modal__content--active');
                  trigger[i].style.transform = 'none';
          trigger[i].style.webkitTransform = 'none';
                  trigger[i].classList.remove('modal__trigger--active');
              }
  
        // when the temporary div is opacity:1 again, we want to remove it from the dom
              div.addEventListener('transitionend', removeDiv, false);
  
        isOpen = false;
  
      }
  
      function removeDiv() {
        setTimeout(function() {
          window.requestAnimationFrame(function() {
            // remove the temp div from the dom with a slight delay so the animation looks good
            div.remove();
          });
        }, contentDelay - 50);
      }
  
    };
  
    var bindActions = function() {
      for (var i = 0; i < len; i++) {
        trigger[i].addEventListener('click', getId, false);
        closers[i].addEventListener('click', close, false);
        modalsbg[i].addEventListener('click', close, false);
      }
    };
  
    var init = function() {
      bindActions();
    };
  
    return {
      init: init
    };
  
  }());
  
  Modal.init();

  $(function() {
    var Accordion = function(el, multiple) {
      this.el = el || {};
      this.multiple = multiple || false;
  
      // Variables privadas
      var links = this.el.find('.link');
      // Evento
      links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
    }
  
    Accordion.prototype.dropdown = function(e) {
      var $el = e.data.el;
        $this = $(this),
        $next = $this.next();
  
      $next.slideToggle();
      $this.parent().toggleClass('open');
  
      if (!e.data.multiple) {
        $el.find('.submenu').not($next).slideUp().parent().removeClass('open');
      };
    }	
  
    var accordion = new Accordion($('#accordion'), false);
  });
  
   
// fix modal window checkbox problem 
  jQuery("#modal2 input:checkbox,.modal label").on("click", function(e)
{
    e.stopImmediatePropagation();
    var element = (e.currentTarget.htmlFor !== undefined) ? e.currentTarget.htmlFor : e.currentTarget;
    var checked = (element.checked) ? false : true;
    element.checked = (checked) ? false : checked.toString();
});  