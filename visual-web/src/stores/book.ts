import { sum } from 'element-plus/es/components/table-v2/src/utils.mjs'
import {defineStore} from 'pinia'
import {computed, ref} from 'vue'

interface BookItem{
    book_id:number
    book_name:string
    book_price:number
    num:number
}

export const userBookStore = defineStore('book',()=>{
    const bookList=ref<BookItem[]>([])

    const bookslen=computed(()=>bookList.value.length)

    const totalPrice=computed(()=>{
        return bookList.value.reduce((sum,x)=>{
            return sum+x.book_price*x.num
        },0)
    })

    function addBook(item:Omit<BookItem, 'num'>){
        const idx=bookList.value.findIndex(i=>i.book_id==item.book_id)
        if(idx>-1){
            bookList.value[idx]!.num = (bookList.value[idx]!.num ?? 0) + 1
        }else{
            bookList.value.push({...item,'num':1})
        }
    }

    return {
        bookList,
        bookslen,
        totalPrice,
        addBook
    }
})