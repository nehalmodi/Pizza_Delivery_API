import streamlit as st
import requests

def run():
    username = st.session_state["username"]
    access_token = st.session_state["access_token"]
    refresh_token = st.session_state["refresh_token"]

    st.write(f"#### Welcome {username}")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    left,right = st.columns([1,1])
    
    with left:
        pizza_size = st.selectbox("Pizza Size",["SMALL","MEDIUM","LARGE"],index=0)
    with right:
        pizza_quantity = st.number_input("QUANTITY",1,50,1)
    
    st.write("")
    order_block = st.columns([1.5,1,1])
  
    if order_block[1].button("Order"):
        order_pizza = requests.post(
            "http://13.233.194.53:8000/orders/order",
            json={
                "quantity": str(pizza_quantity),
                "pizza_size": pizza_size
            },
            headers={
                "Authorization":f"Bearer {access_token}"
            }
        ).json()

        st.success("Orederd Successfully")

    st.write("")

    st.write("******************************")

    after_order = st.columns([1,1,1,1])

    if after_order[0].button("List all Order"):
        list_order = requests.get(
            "http://13.233.194.53:8000/orders/orders",
            headers={
                "Authorization" : f"Bearer {access_token}"
            }
            ).json()

        st.write(list_order)

    with after_order[1]:        
        if st.checkbox("Order by orderid"):
            order_id = st.number_input("order_id",1,1000000,1)
            if st.button("Submit"):
                order_by_id = requests.get(
                    f"http://13.233.194.53:8000/orders/orders/{order_id}",
                    headers={
                         "Authorization" : f"Bearer {access_token}"
                    }
                ).json()
                if "detail" in order_by_id :
                    st.write(order_by_id)
                    st.error("You are not an Admin")
                else:
                    st.write(order_by_id)


    with after_order[2]:
        if st.button("My_Orders"):
            my_order = requests.get(
                "http://13.233.194.53:8000/orders/user/orders",
                headers={
                    "Authorization" : f"Bearer {access_token}"
                }
                ).json()
            st.write(my_order)
            
    
    with after_order[3]:
        if st.checkbox("My_specific_order"):
            new_order_id = st.number_input("order_id",0,10000000,0)
            if st.button("Submit"):
                My_specific_order = requests.get(
                    f"http://13.233.194.53:8000/orders/user/orders/{new_order_id}",
                    headers={
                        "Authorization" : f"Bearer {access_token}"
                    }
                    ).json()
                st.write(My_specific_order)
    st.write("******************************")
    
    update_order = st.columns([1,1.5,1,0.5])

    with update_order[1]:
        if st.checkbox("Update order"):
            oid = st.number_input("Order id",0,100000,0)
            pquantity = st.number_input("Quanity")
            psize = st.selectbox("Pizza Size",["SMALL","MEDIUM","LARGE"],index=0,key="abra")
            if st.button("Submit",key="kad"):
                updater = requests.put(
                    f"http://13.233.194.53:8000/orders/order/update/{oid}",
                    json={
                        "quantity": pquantity,
                        "pizza_size": psize
                    },
                    headers={
                        "Authorization" : f"Bearer {access_token}"
                    }).json()

                st.success("Order updated successfully")

    with update_order[2]:
        if st.checkbox("Update status"):
            uid = st.number_input("Order id",0,100000,0,key="aaaaa")
            order_status = st.selectbox("Pizza Size",["PENDING","IN-TRANSIT","DELIVERED"],index=0)
            if st.button("Submit",key="kaaallaa"):
                updater2 = requests.patch(
                    f"http://13.233.194.53:8000/orders/order/update/{uid}/",
                    json={
                    	"order_status" : order_status
                    },
                    headers={
                        "Authorization" : f"Bearer {access_token}"
                    }).json()

                st.success("Status updated successfully")

    st.write("******************************")
    delete_block = st.columns([1.36,1,1])
    
    with delete_block[1]:

        if st.button("Delete",key="mmmmkaaallaa"):
            did = st.number_input("Order id",0,100000,0,key="mmaaaaa")
            updater2 = requests.patch(
                    f"http://13.233.194.53:8000/orders/order/delete/{id}/",
                    headers={
                        "Authorization" : f"Bearer {access_token}"
                    }).json()

            st.success("Order deleted Successfully")







